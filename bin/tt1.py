import os,sys
from datetime import datetime
import time

import pylab

MINDF = 80
WINDOW=30
keys=('waterheater2:basement', 'l004:kitchen', 'dishwasher:kitchen', 'l021:upstairs',
      'l012:nursery', 'oven:kitchen', 'humidifier1:upstairs', 'uptoilet:upstairs',
      'kitchensink:kitchen', 'l011:bedroom', 'microwave:kitchen', 'l002:kitchen',
      'shower:bathroom', 'downtoilet:bathroom', 'l009:diningroom', 'upsink:upstairs', 'l010:hallway',
      'hairdryer:bathroom', 'l005:kitchen', 'l013:mudroom', 'disposal:kitchen', 'washingmachine:basement',
      'l019:kitchen', 'l018:livingroom', 'toaster:kitchen', 'downsink:bathroom', 'l007:bathroom', 'l014:livingroom',
      'heatingindoorunit:house', 'fridge:kitchen', 'l006:kitchen', 'dryer:basement', 'heatingoutdoorunit:house')

last = None
clist = []

devices=[]
for line in open("ss.csv"):
    datas=[ int(x) for x in line.rstrip().split("\t") ]
    devices.append((datas[0],datas[2]+1))
    devices.append((datas[1],-datas[2]-1))

devices=sorted(devices,key=lambda d : d[0])
idx = 0
for line in open("electric.csv"):
    datas=[ int(x) for x in line.rstrip().split("\t") ]

    if last is not None and datas[0] - last[0] < 5 and abs(datas[1] - last[1]) >= MINDF:
        clist.append((last[0],datas[0] - last[0] , datas[1] - last[1]))
    elif len(clist) > 0 :
        total = clist[0][2]
        while devices[idx][0] < clist[0][0] - WINDOW :
            idx += 1
        iidx = idx
        store=[]
        while devices[iidx][0] < clist[-1][0] + clist[-1][1] + WINDOW :
            store.append(iidx)
            # print "\t",devices[iidx][0] , devices[iidx][1] , keys[abs(devices[iidx][1])-1]
            iidx += 1
        if len(store) == 1 :
            iidx = store[0]
            print clist[0][0],clist[0][1],clist[0][2],
            for node in clist[1:]:
                print node[1],node[2],
                total += node[2]
            print " -> " , total
            print "\t",devices[iidx][0] , devices[iidx][1] , keys[abs(devices[iidx][1])-1]
            print "-" * 30
        clist = []
        # print last[0],datas[0] - last[0] , datas[1] - last[1]
    last = datas
