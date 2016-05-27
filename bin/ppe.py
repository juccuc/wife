__author__ = 'yaowei'
import os,sys
from datetime import datetime

frm='%Y-%m-%d %H:%M:%S'
basetime=datetime.strptime("2014-01-01 00:00:00",frm)
times=[]
min=0 # record from 0
COUNT=5000
c=0
for line in open("../datas/exportedFromMatlab/study10electric1TimesStr.data"):
    if c < min :
        c += 1
        continue
    times.append(int((datetime.strptime(line[19:-1].replace("\t"," "),frm) - basetime).total_seconds()))
    if len(times) >= COUNT :
        break

values=[]
c=0
for line in open("../datas/exportedFromMatlab/study10electric1values.data"):
    if c < min :
        c += 1
        continue
    values.append(int(line.rstrip()))
    if len(values) >= COUNT:
        break
index = 0

c=0
for line in open("../datas/exportedFromMatlab/study10electric2values.data"):
    if c < min :
        c += 1
        continue
    values[index] += int(line.rstrip())
    index += 1
    if index >= COUNT: break

for index in xrange(0,len(times)):
    print "%d\t%d" % (times[index],values[index])

from pylab import *
plot(np.array(times),np.array(values))
# plot([5000],[10000],marker='+', color='r', ls='')
opens=[]
closes=[]
values=[]
texts=[]
for line in open("ss.csv"):
    data=line.rstrip().split("\t")
    st=int(data[0])
    ed=int(data[1])
    idx=int(data[2])
    if st < times[0] and ed < times[0] : continue
    if st > times[-1] and ed > times[0] :
        continue
    plot([st,ed],[500+idx*500,500+idx*500],'k-')
    plot([st,st],[2000,16000],'k--')
    plot([ed,ed],[2000,16000],'k--')

    opens.append(st)
    values.append(500+idx*500)
    closes.append(ed)
    texts.append(idx)
# plot(opens,values,marker='+',color='r',ls='')
# plot(closes,values,marker='x',color='r',ls='')

keys=('waterheater2:basement', 'l004:kitchen', 'dishwasher:kitchen', 'l021:upstairs',
      'l012:nursery', 'oven:kitchen', 'humidifier1:upstairs', 'uptoilet:upstairs',
      'kitchensink:kitchen', 'l011:bedroom', 'microwave:kitchen', 'l002:kitchen',
      'shower:bathroom', 'downtoilet:bathroom', 'l009:diningroom', 'upsink:upstairs', 'l010:hallway',
      'hairdryer:bathroom', 'l005:kitchen', 'l013:mudroom', 'disposal:kitchen', 'washingmachine:basement',
      'l019:kitchen', 'l018:livingroom', 'toaster:kitchen', 'downsink:bathroom', 'l007:bathroom', 'l014:livingroom',
      'heatingindoorunit:house', 'fridge:kitchen', 'l006:kitchen', 'dryer:basement', 'heatingoutdoorunit:house')

for idx in texts:
    text(times[0]-10000,idx*500+500,keys[idx])

show()
