import os,sys
from datetime import datetime
import time

datas=[]

frm='%Y-%m-%d %H:%M:%S.%f'
basetime=datetime.strptime("20")
for line in open("../datas/Study10GroundTruth.csv"):
    data=line.rstrip().lstrip().split(",")
    data=[
        datetime.strptime(data[0],frm),
        datetime.strptime(data[1],frm),
        data[2] + "," + data[3]
    ]
    if len(datas) == 0 or datas[-1][2] != data[2]:
        datas.append(data)
        continue
    pdata=datas[-1]
    if data[0] <= pdata[0] and data[1] >= pdata[0] :
        pdata[0] = data[0]
        if data[1] > pdata[1] :
            pdata[1] = data[1]
        continue
    if pdata[0] <= data[0] and pdata[1] >= data[0]:
        if data[1] > pdata[1]:
            pdata[1] = data[1]
        continue
    datas.append(data)
f=open("s01.csv","w")
for data in datas:
    f.write("%s,%s,%s\n"%(data[0].strftime(frm),data[1].strftime(frm),data[2]))
f.close()

