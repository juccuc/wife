__author__ = 'yaowei'
import os,sys
from datetime import datetime

frm='%Y-%m-%d %H:%M:%S'
basetime=datetime.strptime("2014-01-01 00:00:00",frm)
times=[]
min=24000 # record from 0
COUNT=100000
c=0
for line in open("../datas/exportedFromMatlab/study10waterColdTimesStr.data"):
    if c < min :
        c += 1
        continue
    times.append(int((datetime.strptime(line[19:-1].replace("\t"," "),frm) - basetime).total_seconds()))
    if len(times) >= COUNT :
        break

values=[]
c=0
for line in open("../datas/exportedFromMatlab/study10waterColdvalues.data"):
    if c < min :
        c += 1
        continue
    values.append(float(line.rstrip()))
    if len(values) >= COUNT:
        break
values_h=[]
c=0
for line in open("../datas/exportedFromMatlab/study10waterHotvalues.data"):
    if c < min :
        c += 1
        continue
    values_h.append(float(line.rstrip()))
    if len(values_h) >= COUNT:
        break

from pylab import *
plot(np.array(times),np.array(values),color='b')
plot(np.array(times),np.array(values_h),color='r')

# show()
# sys.exit(1)
# plot([5000],[10000],marker='+', color='r', ls='')
#opens=[]
#closes=[]
#values=[]
#texts=[]
#for line in open("ss.csv"):
    # data=line.rstrip().split("\t")
    # st=int(data[0])
    # ed=int(data[1])
    # idx=int(data[2])
    # if st < times[0] and ed < times[0] : continue
    # if st > times[-1] and ed > times[0] :
    #     continue
    # plot([st,ed],[idx*0.05,idx*0.05],'k-',picker=5)
    # plot([st,st],[-2,3],'k--')
    # plot([ed,ed],[-2,3],'k--')
    #
    # opens.append(st)
    # values.append(idx*0.05)
    # closes.append(ed)
    # texts.append(idx)
# plot(opens,values,marker='+',color='r',ls='')
# plot(closes,values,marker='x',color='r',ls='')

keys=('waterheater2:basement', 'l004:kitchen', 'dishwasher:kitchen', 'l021:upstairs',
      'l012:nursery', 'oven:kitchen', 'humidifier1:upstairs', 'uptoilet:upstairs',
      'kitchensink:kitchen', 'l011:bedroom', 'microwave:kitchen', 'l002:kitchen',
      'shower:bathroom', 'downtoilet:bathroom', 'l009:diningroom', 'upsink:upstairs', 'l010:hallway',
      'hairdryer:bathroom', 'l005:kitchen', 'l013:mudroom', 'disposal:kitchen', 'washingmachine:basement',
      'l019:kitchen', 'l018:livingroom', 'toaster:kitchen', 'downsink:bathroom', 'l007:bathroom', 'l014:livingroom',
      'heatingindoorunit:house', 'fridge:kitchen', 'l006:kitchen', 'dryer:basement', 'heatingoutdoorunit:house')

# for idx in texts:
#     text(times[0]-1000,idx*0.05,keys[idx])

def onClick(event):
    xdata = event.xdata
    ydata = event.ydata
    print 'onpick points:', (xdata, ydata)
figure(1).canvas.mpl_connect('button_press_event',onClick)
show()
