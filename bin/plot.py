#!/usr/bin/python
import sys,os
from pylab import plot,show,xlabel,ylabel
import argparse

parser = argparse
DT = 3
def readFileData(filename):
    datas=[]
    for line in open(filename):
        data = [int(x) for x in line.rstrip().split("\t")]
        if len(datas) > 0 and data[0] > datas[-1][0] + DT and data[1] != datas[-1][1] :
            datas.append([data[0] - DT , datas[-1][1]])
        datas.append(data)
    return datas

for filename in sys.argv[1:]:
    if os.path.isfile(filename):
        datas = zip(*readFileData(filename))
        plot(datas[0],datas[1])
xlabel("Duration from a specific time (Second)")
ylabel("Power (W)")
show()


