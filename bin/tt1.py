import os,sys
from datetime import datetime
import time

datas=[]

frm='%Y-%m-%d %H:%M:%S.%f'
f=open("s02.csv","w")

for line in open("s01.csv"):
    data=line.rstrip().lstrip().split(",")
    data=[
        datetime.strptime(data[0],frm),
        datetime.strptime(data[1],frm),
        data[2] + "," + data[3]
    ]
    # if len(datas) > 0 and datas[-1][0] > data[0]:
    #     print "error",line
    #
    # datas.append(data)

    if data[0] >= data[1] :
        print "error",line[:-1]
    else:
        f.write(line)
f.close()
