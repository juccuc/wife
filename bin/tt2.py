
datas=[]
times=[]
values=[]
st=None
for line in open("electric.csv"):
    datas.append([int(x) for x in line.rstrip().split("\t")])
    if st is None :
        times.append(0)
        st = datas[-1][0]
    else:
        times.append(datas[-1][0]-st)
    values.append(datas[-1][1])

WINDOW=20
ndatas=[]

idx = 0

for t in xrange(datas[0][0],datas[-1][0]):
    while idx < len(datas) and datas[idx][0] < t - WINDOW : idx += 1
    total=[]
    iidx = idx
    while iidx < len(datas) and datas[iidx][0] < t + WINDOW :
        total.append(datas[iidx][1])
        iidx += 1
    if len(total) > 0 :
        ndatas.append(reduce(lambda x, y: x + y, total) / len(total))
    else:
        ndatas.append(-1)
from pylab import *

from pylab import *
plot(np.arange(len(ndatas)),np.array(ndatas))
plot(np.array(times),np.array(values))
show()
