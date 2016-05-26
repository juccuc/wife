#! -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime

keys=('waterheater2:basement', 'l004:kitchen', 'dishwasher:kitchen', 'l021:upstairs',
      'l012:nursery', 'oven:kitchen', 'humidifier1:upstairs', 'uptoilet:upstairs',
      'kitchensink:kitchen', 'l011:bedroom', 'microwave:kitchen', 'l002:kitchen',
      'shower:bathroom', 'downtoilet:bathroom', 'l009:diningroom', 'upsink:upstairs', 'l010:hallway',
      'hairdryer:bathroom', 'l005:kitchen', 'l013:mudroom', 'disposal:kitchen', 'washingmachine:basement',
      'l019:kitchen', 'l018:livingroom', 'toaster:kitchen', 'downsink:bathroom', 'l007:bathroom', 'l014:livingroom',
      'heatingindoorunit:house', 'fridge:kitchen', 'l006:kitchen', 'dryer:basement', 'heatingoutdoorunit:house')

frm='%Y-%m-%d %H:%M:%S.%f'
basetime=datetime.strptime("2014-01-01 00:00:00.000000",frm)
f=open("ss.csv","w")
for line in open("s02.csv"):
    data=line.rstrip().split(",")
    start = ( datetime.strptime(data[0],frm) - basetime ).total_seconds()
    end = ( datetime.strptime(data[1],frm) - basetime ).total_seconds()
    index = keys.index(data[2].lower() + ":" + data[3].lower())
    # keys.add(key[0].lower() + ":" + key[1].lower())
    f.write("%d\t%d\t%d\n" % (int(start),int(end),index))
f.close()
print len(keys),keys