import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random 
def processing(M):
    #total=0
    L=[]
    H=[]
    for i in M:
        if i.isdigit():
            L.append(int(i))
        else:
<<<<<<< HEAD
             L.append(int(99999999))
=======
            L.append(int(9999999999))
>>>>>>> f475e2652221f4cf0edacac7b26de5d35917eb0a
    P=np.percentile(L,99)
    for i in L:
        if i <= int(P):
            H.append(int(i))
        else:
            H.append(int(P))
    return H
<<<<<<< HEAD
=======
#the data dir

>>>>>>> f475e2652221f4cf0edacac7b26de5d35917eb0a
g = os.walk("test_KVM_4_13_nonovercommit")
ref=[]
files=[]
for path,dir_list,file_list in g:  
    for file_name in file_list:  
        out = (os.path.join(path, file_name) )
        files.append(out)
        out = out.split('/')
        ref.append(out[1:])

timectxsw=[[] for i in range(13)]
timetctxsw=[[] for i in range(13)]
timetctxsw2=[[] for i in range(13)]
timesyscall=[[] for i in range(13)]
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
    

for i in timetctxsw2:
    print(len(i))
for i in timetctxsw:
    print(len(i))
for i in timectxsw:
    print(len(i))
for i in timesyscall:
    print(len(i))

<<<<<<< HEAD
_timectxsw=np.array(timectxsw)
_timetctxsw=np.array(timetctxsw)
_timetctxsw2=np.array(timetctxsw2)
_timesyscall=np.array(timesyscall)
=======
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
>>>>>>> f475e2652221f4cf0edacac7b26de5d35917eb0a

timectxsw=pd.DataFrame(data=_timectxsw.T,columns=list(range(1,14)))
ax = sns.violinplot(data=timectxsw,scale='area')
timectxsw=pd.DataFrame(data=_timectxsw.T,columns=list(range(0,13)))
sns.lineplot(data=timectxsw.mean())
plt.savefig('pdf/timectxsw.pdf')
plt.clf()

timetctxsw=pd.DataFrame(data=_timetctxsw.T,columns=list(range(1,14)))
ax = sns.violinplot(data=timetctxsw)
timetctxsw=pd.DataFrame(data=_timetctxsw.T,columns=list(range(0,13)))
sns.lineplot(data=timetctxsw.mean())
plt.savefig('pdf/timetctxsw.pdf')
plt.clf()

timetctxsw2=pd.DataFrame(data=_timetctxsw2.T,columns=list(range(1,14)))
ax = sns.violinplot(data=timetctxsw2)
timetctxsw2=pd.DataFrame(data=_timetctxsw2.T,columns=list(range(0,13)))
sns.lineplot(data=timetctxsw2.mean())
plt.savefig('pdf/timetctxsw2.pdf')
plt.clf()

timesyscall=pd.DataFrame(data=_timesyscall.T,columns=list(range(1,14)))
ax = sns.violinplot(data=timesyscall)
timesyscall=pd.DataFrame(data=_timesyscall.T,columns=list(range(0,13)))
sns.lineplot(data=timesyscall.mean())
plt.savefig('pdf/timesyscall.pdf')
plt.clf()
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

