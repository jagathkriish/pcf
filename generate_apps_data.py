import subprocess
import shlex
import json
import datetime
import time
import xlsxwriter

api = ''
user = ''
pwd = ''
org = ''
space = ''
login_command = 'cf login -a ' + api + ' -u ' + user + ' -p ' + pwd + ' -o ' + org + ' -s ' + space + ' --skip-ssl-validation'
list_all_orgs = 'cf curl /v2/organizations'+'?results-per-page=500'
timestamp_str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')

#running cf login shell command for login and running commands
process = subprocess.Popen(shlex.split(login_command), stdout=subprocess.PIPE)
login_output = process.communicate()[0]
print(login_output)

#listing all orgs
process = subprocess.Popen(shlex.split(list_all_orgs), stdout=subprocess.PIPE)
raw_org_json = process.communicate()[0]
org_json = json.loads(raw_org_json)
print(org_json['total_results'])
for org_obj in org_json['resources']:
    workbook = xlsxwriter.Workbook(org_obj['entity']['name']+'_'+timestamp_str+'.xlsx')
    bold = workbook.add_format({'bold': True})
    cf_list_spaces_command = 'cf curl '+org_obj['entity']['spaces_url']+'?results-per-page=500'
    process = subprocess.Popen(shlex.split(cf_list_spaces_command), stdout=subprocess.PIPE)
    raw_spaces_json = process.communicate()[0]
    spaces_json = json.loads(raw_spaces_json)
    for space_obj in spaces_json['resources']:
        sheetName = ''
        if(len(space_obj['entity']['name']) > 31):
            sheetName = space_obj['entity']['name'][:29]+'..'
        else:
            sheetName = space_obj['entity']['name'][:31]
        worksheet = workbook.add_worksheet(sheetName)
        worksheet.write('A1', 'Organization:', bold)
        worksheet.write('A2', org_obj['entity']['name'])
        worksheet.write('A4', 'Space', bold)
        worksheet.write('A5', space_obj['entity']['name'])
        cf_list_apps_command = 'cf curl '+space_obj['entity']['apps_url']+'?results-per-page=500'
        process = subprocess.Popen(shlex.split(cf_list_apps_command), stdout=subprocess.PIPE)
        raw_apps_json = process.communicate()[0]
        apps_json = json.loads(raw_apps_json)
        worksheet.write('A7', 'Applications', bold)
        worksheet.write('A8', 'Name', bold)
        worksheet.write('B8', 'Memory', bold)
        worksheet.write('C8', 'Instances', bold)
        worksheet.write('D8', 'Disk space', bold)
        worksheet.write('E8', 'State', bold)
        row = 9
        col = 0
        for app in apps_json['resources']: 
            worksheet.write(row, col,     app['entity']['name'])
            worksheet.write(row, col + 1, app['entity']['memory'])
            worksheet.write(row, col + 2, app['entity']['instances'])
            worksheet.write(row, col + 3, app['entity']['disk_quota'])
            worksheet.write(row, col + 4, app['entity']['state'])
            row += 1
    workbook.close()
