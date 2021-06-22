# replay_tools

The replay tools are very easy, leverage on cgroup. 

pre-requisites: linux cgroup support -> cpu, blkio, network_cls

How to play with this easy tool? 
with sudo all the time is needed
1. online all cgroup
```
sh cpu/cgroup_init.sh
sh network/cgroup_init.sh $nic_interface #for example, sh network/cgroup_init.sh ens3
sh diskio/cgroup_init.sh
```
2. set up network sender on host to replay the rx
put the dir network/ to some place
```
scp -r network kone:~
``` 
3. set up the origin csv
```
we have three python scripts and a C program, each of them will read a csv file as input.
1. process.py -> record.csv and cpu_overhead.csv
2. process_no_cpu.py -> record.csv
3. network/host_rx.py -> rx.csv
4. memory/memory_replay.c -> memory_record

for all python scripts, you have to tell which raw of virt-top output vm is the one you going to replay.
PLease open the script and change the $Var on the top line. The number start with 1 instead of 0!!!

there is a helper.py to help you check which raw. helper.py will print the data of the raw you have choosen. 

for C program, the a.out is the exeutable file, the memory_record is the file from the wasted_log_lib/analyze-results/cloudRep_{500,250,100,50,3}ms/processed/vm1/mem_usage_vm.log

all input files please put AT SAME PLACE with the scripts or executable

```
4. replay without cpu
```
To replay without cpu
Please checkout host_rx.py and also change the IP address of the guest vm that going to replay.

from inside: 
sudo sh python3 process_no_cpu.py
outside:
sudo sh python3 host_rx.py

In the meanwhile you should start record. 

After run REMEMBER TO CLEAN THE MACHINES! USE KILL or KILLALL.

```
After run REMEMBER TO CLEAN THE MACHINES! USE KILL or KILLALL.

5. replay with cpu
```
The record of replay without cpu csv file should rename as cpu_overhead.csv
which has the cpu overhead of others replay. 
Please also tell the raw of the vm, and remember, this time, the raw should be the vm that just run the replay without cpu
instead of the original vm that we are going to fake.
you still can use helper to check if you are not sure. The number start with 1 instead of 0!!!

REMEMBER TO CLEAN THE MACHINES! USE KILL or KILLALL. 


This time, the replay cpu will minus the replay overhead first then replay.
Then inside:
Please checkout host_rx.py and also change the IP address of the guest vm that going to replay.

sudo sh python3 process.py
outside:
sudo sh python3 host_rx.py 
In the meanwhile you should start record. 


```
