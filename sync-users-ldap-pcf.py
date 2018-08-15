import subprocess
import shlex
import json
import datetime
import time
import xlsxwriter
import ldap

api = ''
user = ''
pwd = ''
org = ''
space = ''

orgs_to_scan = ['ci-org', 'demo-org', 'playground-org', 'qa-org', 'syt-org']
org_group_map = {'ci-org': 'cn=PCF_Sandbox_SpaceDevelopers_CI,ou=test,ou=pcf,ou=groups,ou=enterprise,dc=int,dc=8451,dc=com',
'demo-org': 'cn=PCF_Sandbox_SpaceDevelopers_DEMO,ou=test,ou=pcf,ou=groups,ou=enterprise,dc=int,dc=8451,dc=com',
'playground-org': 'cn=PCF_Sandbox_SpaceDevelopers_PLG,ou=test,ou=pcf,ou=groups,ou=enterprise,dc=int,dc=8451,dc=com',
'qa-org': 'cn=PCF_Sandbox_SpaceDevelopers_QA,ou=test,ou=pcf,ou=groups,ou=enterprise,dc=int,dc=8451,dc=com', 
'syt-org': 'cn=PCF_Sandbox_SpaceDevelopers_SYT,ou=test,ou=pcf,ou=groups,ou=enterprise,dc=int,dc=8451,dc=com'}
ldap_url = 'ldap://localhost:10389'
ldap_bind_dn = u'cn=jagathpathi,ou=users,dc=example,dc=com'
ldap_bind_pw = u'0787'
ldap_user_dn = u'ou=users,dc=example,dc=com'

login_command = 'cf login -a ' + api + ' -u ' + user + ' -p ' + pwd + ' -o ' + org + ' -s ' + space + ' --skip-ssl-validation'
list_all_orgs = 'cf curl /v2/organizations'
timestamp_str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')

#ldap configuration
ldap_con = ldap.initialize(ldap_url, bytes_mode=False)
ldap_con.simple_bind_s(ldap_bind_dn, ldap_bind_pw)

#running cf login shell command for login and running commands
process = subprocess.Popen(shlex.split(login_command), stdout=subprocess.PIPE)
login_output = process.communicate()[0]
print(login_output)

#listing all orgs
process = subprocess.Popen(shlex.split(list_all_orgs), stdout=subprocess.PIPE)
raw_org_json = process.communicate()[0]
org_json = json.loads(raw_org_json)
print(org_json['total_results'])
workbook = xlsxwriter.Workbook('unmatched_user_data_'+timestamp_str+'.xlsx')
bold = workbook.add_format({'bold': True})
worksheet = workbook.add_worksheet("pcf_user_list")
worksheet.write('A1', 'Users in PCF:', bold)
worksheet1 = workbook.add_worksheet("mismatch_Users_list")
worksheet1.write('A1', 'Mismatched Users with Ldap:', bold)
row = 3
col = 0
row1 = 3
col1 = 0
for org_obj in org_json['resources']:
    print('org: '+org_obj['entity']['name'])
    if((org_obj['entity']['name'] in orgs_to_scan) == False):
        print("org not found in scan list skipping: "+org_obj['entity']['name']+"  len: "+str(len(org_obj['entity']['name'])))
        continue
    cf_list_spaces_command = 'cf curl '+org_obj['entity']['spaces_url']
    process = subprocess.Popen(shlex.split(cf_list_spaces_command), stdout=subprocess.PIPE)
    raw_spaces_json = process.communicate()[0]
    spaces_json = json.loads(raw_spaces_json)
    for space_obj in spaces_json['resources']:
        print('space: '+space_obj['entity']['name'])
        cf_list_space_developers_command = 'cf curl '+space_obj['entity']['developers_url']
        process = subprocess.Popen(shlex.split(cf_list_space_developers_command), stdout=subprocess.PIPE)
        raw_space_developers = process.communicate()[0]
        space_developers = json.loads(raw_space_developers)

        dev_usernames = []
        for developer in space_developers['resources']:
            print('developer username: '+developer['entity']['username'])
            if((developer['entity']['username'] in dev_usernames) == False):
                worksheet.write(row, col, developer['entity']['username'])
                row += 1
                dev_usernames.append(developer['entity']['username'])
                results = ldap_con.search_s(ldap_user_dn, ldap.SCOPE_SUBTREE , u"(cn="+developer['entity']['username']+")")
                if(len(results) == 0):
                    if(developer['entity']['username'] != 'admin'):
                        worksheet1.write(row, col1,     developer['entity']['username'])
                        worksheet1.write(row, col1+2,   'not present in user group itself')
                        row1 += 1
                        cf_delete_user_cmd = 'cf delete-user '+developer['entity']['username']+ ' -f'
                        process = subprocess.Popen(shlex.split(cf_delete_user_cmd), stdout=subprocess.PIPE)
                        res_delete = process.communicate()[0]
                        print(res_delete)
                elif (len(results) == 1):
                    if(developer['entity']['username'] != 'admin'):
                        group_to_check = org_group_map[org_obj['entity']['name']]
                        if((group_to_check in results[0][1]['memberOf']) == False):
                            worksheet1.write(row, col1,     developer['entity']['username'])
                            worksheet1.write(row, col1+2,   group_to_check)
                            row1 += 1
                            cf_delete_user_cmd = 'cf delete-user '+developer['entity']['username']+ ' -f'
                            process = subprocess.Popen(shlex.split(cf_delete_user_cmd), stdout=subprocess.PIPE)
                            res_delete = process.communicate()[0]
                            print(res_delete)
workbook.close()
