import csv
import time
import os
import subprocess
from itertools import islice

#########################################
#########################################
measurements_time=1
run_time="600"
nic_name="br1"
major=10
replay_raw=[]
iperf_target_ip=[]
iperf_server_port=[]
cgroup_minor_num=[]
#########################################
#########################################
with open('config_host', newline='', encoding='utf-8') as config:
    for row in config:
        row=row.split()
        iperf_target_ip.append(row[0])
        iperf_server_port.append(row[1])
        cgroup_minor_num.append(row[2])
        replay_raw.append(row[3])
number_of_machines=len(iperf_target_ip)
print(number_of_machines)
vm_time=[]
with open('rx.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in islice(reader, 1, None):
        vm=[[0 for x in range(6)] for y in range(10)]
        c=0
        for i in range(19,len(row)-1):
            if (i-19)%10==0:
                vm[c][0]=row[i+2]
                vm[c][1]=row[i+4]
                vm[c][2]=row[i+5]
                vm[c][3]=row[i+6]
                vm[c][4]=row[i+7]
                vm[c][5]=row[i+8]
                c+=1
        vm_time.append(vm)
def network_rx_of_vm(i):
    rx=[]
    if i==0:
        i=1
    for vv in vm_time:
        rx.append(vv[i-1][4])
    return rx

def network_change(i,major,minor):
    if i == '':
        return 
    j=int(i)
    j=int((j*8)/(1024*measurements_time))
    if j == 0:
        j=1000
    i = str(j)
    cmd="sudo tc class change dev "+str(nic_name)+" parent "+str(major)+": classid "+str(major)+":"+str(minor)+" htb rate "+ i+"kbit"
    #print(cmd)
    subprocess.Popen(cmd,shell=True,stdout=None)
c=0


def init():
    for i in range(0,number_of_machines):
        network_rx_cmd = "sudo iperf -s -u -p "+iperf_server_port[i]
        #print(network_rx_cmd)
        subprocess.Popen(network_rx_cmd,shell=True,stdout=None)
    time.sleep(3)
    for i in range(0,number_of_machines):
        network_tx_cmd = "sudo cgexec -g net_cls:replay"+cgroup_minor_num[i]+" iperf -c "+iperf_target_ip[i]+"  -t "+run_time+" -u -b 100mb"
        #print(network_tx_cmd)
        subprocess.Popen(network_tx_cmd,shell=True,stdout=None)

rx=[]
for i in replay_raw:
    rx.append(network_rx_of_vm(int(i)))
print("Please remember sudo")
init()
for i in range(0,len(rx[0])):
    start=time.time()
    for j in range(0,number_of_machines):
        network_change(rx[j][i],major,cgroup_minor_num[j])
    end=time.time()
    if end-start<measurements_time:
        time.sleep(measurements_time-(end-start))

