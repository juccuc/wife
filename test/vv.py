from pylab import *

datas=[]
for line in open("../datas/exportedFromMatlab/study10electric1values.data"):
    datas.append(float(line.rstrip().lstrip()))
index=0
for line in open("../datas/exportedFromMatlab/study10electric2values.data"):
    datas[index] += float(line.rstrip().lstrip())
    index += 1

plot(np.array(datas[:50000]))
axhline(linewidth=4)

# plot(np.array(datas[500:1000]))
# axis([0,500,0,60000])
show()
#print len(datas),datas[:5]
