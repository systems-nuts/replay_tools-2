import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#make sure all data is digital 
def processing(M):
    #total=0
    L=[]
    H=[]
    for i in M:
        if i.isdigit():
            L.append(int(i))
    P=np.percentile(L,99)
    for i in L:
        if i <= int(P):
            H.append(int(i))
        else:
            H.append(int(P))
    return H
#the data dir

g = os.walk("test_KVM_4_13_nonovercommit")

ref=[]
files=[]
for path,dir_list,file_list in g:  
    for file_name in file_list:  
        out = (os.path.join(path, file_name) )
        files.append(out)
        out = out.split('/')
        ref.append(out[1:])
#output list, for 13 vm, for 4vm you should change it to *4
timectxsw=[[]]*13
timetctxsw=[[]]*13
timetctxsw2=[[]]*13
timesyscall=[[]]*13
# put all data in one list
# for example, 13 vm with 4cpu, there will be 13 index for each list, and 4cpu data will be 
# extend into this list and we will caculate the average later.
# for example, timetctxsw2[] will have 13, and each index contain 4vcpus data. 
# 
for i,j in zip(ref,files):
    index=i[0]
    exactly=i[2]
    print(index, exactly)
    f = open(j)
    tmp = (f.read().splitlines())
    tmp = processing(tmp)
    if exactly == "timetctxsw2.out":
        timetctxsw2[int(index)-1].extend(tmp)
    elif exactly == "timetctxsw.out":
        timetctxsw[int(index)-1].extend(tmp)
    elif exactly == "timectxsw.out":
        timectxsw[int(index)-1].extend(tmp)
    else:
        timesyscall[int(index)-1].extend(tmp)
    f.close()
    
#check the size
for i in timetctxsw2:
    print(len(i))
for i in timetctxsw:
    print(len(i))
for i in timectxsw:
    print(len(i))
for i in timesyscall:
    print(len(i))
    


# create data frame, please make sure all the origin data is same size. otherwise there is bug.
timectxsw=np.array(timectxsw)
timetctxsw=np.array(timetctxsw)
timetctxsw2=np.array(timetctxsw2)
timesyscall=np.array(timesyscall)

# range also need to change
timectxsw=pd.DataFrame(data=timectxsw.T,columns=list(range(1,14)))
timetctxsw=pd.DataFrame(data=timetctxsw.T,columns=list(range(1,14)))
timetctxsw2=pd.DataFrame(data=timetctxsw2.T,columns=list(range(1,14)))
timesyscall=pd.DataFrame(data=timesyscall.T,columns=list(range(1,14)))

ax = sns.violinplot(data=timectxsw)
plt.savefig('test_KVM_4_13_nonovercommit/timectxsw.pdf')
ax = sns.violinplot(data=timetctxsw)
plt.savefig('test_KVM_4_13_nonovercommit/timetctxsw.pdf')
ax = sns.violinplot(data=timetctxsw2)
plt.savefig('test_KVM_4_13_nonovercommit/timetctxsw2.pdf')
ax = sns.violinplot(data=timesyscall)
plt.savefig('test_KVM_4_13_nonovercommit/timesyscall.pdf')
#print(processing(output[3][0]))
'''
r=[]
for i in output:
    for j in i:
        r.append(processing(j))
for i in range(0,len(r)):
    if i % 4 ==0 and i != 0:
        print("")
    print(r[i][0],",",r[i][1],",",r[i][2])
'''

