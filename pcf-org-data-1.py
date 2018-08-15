import subprocess
import shlex

login_command = ''
list_all_orgs = 'cf orgs'
list_space_users = ''
api = ''
user = ''
pwd = ''

process = subprocess.Popen(shlex.split(login_command), stdout=subprocess.PIPE)
stdout = process.communicate()[0]
print(stdout)
process = subprocess.Popen(shlex.split(list_all_orgs), stdout=subprocess.PIPE)
stdout1 = process.communicate()[0]
org_list = stdout1.split('name')[1].strip().split("\n")
print(org_list)
process = subprocess.Popen(shlex.split("cf org "+org_list[0]), stdout=subprocess.PIPE)
raw_org_data = process.communicate()[0]
space_list = raw_org_data.split("spaces:")[1].strip().replace("isolation segments:","").strip().split(',')
print(raw_org_data)
for space in space_list:
    login_specific_org_space = "cf login -a " + api + " -u " + user + " -p " + pwd + " -o " + org_list[0] + " -s " + space + " --skip-ssl-validation"
    process = subprocess.Popen(shlex.split(login_specific_org_space), stdout=subprocess.PIPE)
    login_org_space = process.communicate()[0]
    print(login_org_space)
    process = subprocess.Popen(shlex.split("cf apps"), stdout=subprocess.PIPE)
    apps_list = process.communicate()[0] 
    print(apps_list)