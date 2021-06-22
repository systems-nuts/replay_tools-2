import csv
import time
import os
import subprocess
from itertools import islice
#########################################
#########################################
which_row_of_replay_csv=2
which_row_of_cpu_over_head_csv=8
guest_ip_address="192.168.10.54"
#########################################
#########################################

vm_time=[]
with open('rx.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in islice(reader, 1, None):
        vm=[[0 for x in range(6)] for y in range(8)]
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
#print(vm_time)
def print_log():
    for vv in vm_time:
        for i in range(0,len(vv)):
            #print("vm"+str(i+1),end=' ')
            for j in vv[i]:
                print(j,' ',end='')
            print()
        print()

def cpu_of_vm(i):
    cpu=[]
    if i==0:
        i=1
    for vv in vm_time:
        cpu.append(vv[i-1][0])
    return cpu
def network_rx_of_vm(i):
    rx=[]
    if i==0:
        i=1
    for vv in vm_time:
        rx.append(vv[i-1][4])
    return rx
def network_tx_of_vm(i):
    tx=[]
    if i==0:
        i=1
    for vv in vm_time:
        tx.append(vv[i-1][5])
    return tx

def disk_read_of_vm(i):
    read=[]
    if i==0:
        i=1
    for vv in vm_time:
        read.append(vv[i-1][2])
    return read
def disk_write_of_vm(i):
    write=[]
    if i==0:
        i=1
    for vv in vm_time:
        write.append(vv[i-1][3])
    return write
def cpu_change(i):
    u=float(i)
    ii=u*100000
    ii=int(ii)
    if ii<=0:
        ii=1000
    cmd="echo "+str(ii)+" >/sys/fs/cgroup/cpu/replay/cpu.cfs_quota_us "
    os.system(cmd)

def disk_io_change(i,j):
    if i == '0':
        i = '1000'
    if j=='0':
        j= '1000'
    cmd1="echo " + "8:0 " + i +" > /sys/fs/cgroup/blkio/replay/blkio.throttle.read_bps_device  "
    cmd2="echo " + "8:0 " + j +" > /sys/fs/cgroup/blkio/replay/blkio.throttle.write_bps_device  "
    os.system(cmd1)
    os.system(cmd2)

def network_change(i):
    if i == '':
        return 
    j=int(i)
    j=int((j*32)/1024)
    if j == 0:
        j=1
    i = str(j)
    cmd="sudo tc class change dev br1 parent 10: classid 10:1 htb rate "+ i+"kbit"
    os.system(cmd)


c=0
def init():
    network_change("10240")
    network_tx_cmd = "sudo cgexec -g net_cls:client ./ITGSend -a " + guest_ip_address + " -T udp -t 1000000 -c 20000"
    print(network_tx_cmd)
    print("please check the guest ip is correct",guest_ip_address)
    network_rx_cmd = "sudo ./ITGRecv"
    subprocess.Popen(network_rx_cmd,shell=True,stdout=None)
    time.sleep(3)
    subprocess.Popen(network_tx_cmd,shell=True,stdout=None)


cpu=cpu_of_vm(which_row_of_replay_csv)
tx=network_tx_of_vm(which_row_of_replay_csv)
rx=network_rx_of_vm(which_row_of_replay_csv)
read=disk_read_of_vm(which_row_of_replay_csv)
write=disk_write_of_vm(which_row_of_replay_csv)
init()
for i in rx:
    network_change(i)
    time.sleep(0.25)

