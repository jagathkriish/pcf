import datetime
import os
import shlex
import subprocess
import time
import xlsxwriter

st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')

server_data = {'ip1': 'username1', 'ip2': 'username2'}
workbook = xlsxwriter.Workbook('machine_memory_details_'+st+'.xlsx')
for server in server_data:
    print(server)
    print(server_data[server])
    worksheet = workbook.add_worksheet(server)
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', server+"\n", bold)
    worksheet.write('A3', "Disk name", bold)
    worksheet.write('B3', "Total size ", bold)
    worksheet.write('C3', "Used ", bold)
    worksheet.write('D3', "Used % ", bold)
    worksheet.write('E3', "mounted path ", bold)
    process1 = subprocess.Popen(shlex.split('ssh '+server_data[server]+'@'+server+' df -h'), stdout=subprocess.PIPE)
    #process1 = subprocess.Popen(shlex.split('df -h'), stdout=subprocess.PIPE)
    stdout1 = process1.communicate()[0]
    disk_list = stdout1.decode().split("\n")
    row=4
    for disk in disk_list[1:]:
        disk_params = disk.split()
        column=0
        if(len(disk_params) != 0):
            worksheet.write(row,column,disk_params[0])
            worksheet.write(row,column+1,disk_params[1])
            worksheet.write(row,column+2,disk_params[3])
            worksheet.write(row,column+3,disk_params[4])
            worksheet.write(row,column+4,disk_params[5])
        row = row + 1

    row = row + 2
    col = 0
    header_col = 'A' + str(row) 
    worksheet.write(header_col, "Top 10 folders ", bold)
    row = row + 2
    cmd = 'ssh -t '+server_data[server]+'@'+server+" 'cd /tc && du -hs * | sort -rh | head -10'"
    top_folder_data = subprocess.check_output(cmd, shell=True)
    top_folder_list = top_folder_data.decode().split("\n")
    
    for folder in top_folder_list[:10]:
        folder_data = folder.split()
        if(len(folder_data) != 0):
            worksheet.write(row,col, folder_data[0])
            worksheet.write(row,col+1, folder_data[1])
        row = row + 1
workbook.close()

file_name = 'machine_memory_details_'+st+'.xlsx'
from_addr = 
to_addr = 
subject = 
body = 
email_cmd = 'echo '+body+' | mail -s '+subject+' -r '+from_addr+' -a '+file_name+' '+to_addr
process2 = subprocess.Popen(shlex.split(email_cmd), stdout=subprocess.PIPE)
stdout2 = process1.communicate()[0]
print(stdout2)
#remove file
process3 = subprocess.Popen(shlex.split('rm '+file_name), stdout=subprocess.PIPE)
stdout3 = process1.communicate()[0]
print(stdout3)
