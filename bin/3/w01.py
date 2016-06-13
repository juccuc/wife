import os,sys
from pylab import *


def readFileData(filename):
    datas=[]
    for line in open(filename):
        data = [int(x) for x in line.rstrip().split("\t")]
        datas.append(data)
    return datas


gt2000=zip(*readFileData("../../datas/a/cold.hot.gt2000"))

plot(gt2000[0],gt2000[1],"ro")

for line in open("../ss.csv"):
    data = [int(x) for x in line.rstrip().split("\t")]
    if data[2] == 12 :
        plot(data[:2],[2000,2000])

show()