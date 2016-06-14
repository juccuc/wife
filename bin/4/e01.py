#!/usr/bin/python

def readFileData(filename):
    datas=[]
    for line in open(filename):
        data = [int(x) for x in line.rstrip().split("\t")]
        datas.append(data)
    return datas

datas=readFileData("../../datas/a/electric01")


count=25
start=False
for idx in xrange(1,len(datas)):
    if datas[idx][0] == 4463131 :
        start = True
    if start :
        print datas[idx][1] - datas[idx-1][1]
        count -= 1
        if count == 0 : break
