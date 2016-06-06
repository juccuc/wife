import os,sys

before=None
times=[]
values=[]
aa=[]
vv=[]
ma=0
counts=[0] * 9

for line in open("electric.csv"):
    data=tuple([ int(x) for x in line.rstrip().split("\t")])
    if before is not None and data[1] - before[1] >= 100:
        times.append(data[0])
        values.append(data[1])
        if len(aa) == 0 : aa.append(before)
        aa.append(data)
    elif len(aa) > 0 :
        for d in aa :
            print d
        print "-"*30,len(aa),data
        vv.append(len(aa))
        if len(aa) > ma : ma =len(aa)
        counts[len(aa)-1] += 1
        aa=[]
    before=data
print ma,vv
print counts
# from pylab import *
# plot(np.array(times),np.array(values))
# show()
