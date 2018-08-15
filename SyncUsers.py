import subprocess
import shlex

login_command = '<>'
list_org_users = ''
list_space_users = ''


process = subprocess.Popen(shlex.split(login_command), stdout=subprocess.PIPE)
stdout = process.communicate()[0]
print(stdout)
process = subprocess.Popen(shlex.split(list_org_users), stdout=subprocess.PIPE)
stdout1 = process.communicate()[0]

print(stdout1)
for i in stdout1.splitlines():
    print(i)