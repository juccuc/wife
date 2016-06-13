#!/usr/bin/python

import argparse


def readFileData(filename):
    datas=[]
    for line in open(filename):
        datas.append([int(x) for x in line.rstrip().split("\t")])
    return datas


parser = argparse.ArgumentParser()
parser.add_argument("first")
parser.add_argument("second")

args = parser.parse_args()

fdatas=readFileData(args.first)
sdatas=readFileData(args.second)

fidx = sidx = 0

fdata=0
sdata=0
while fidx < len(fdatas) and sidx < len(sdatas):
    if fdatas[fidx][0] == sdatas[sidx][0] :
        fdata = fdatas[fidx][1]
        sdata = sdatas[sidx][1]
        print "%d\t%d" % (fdatas[fidx][0],fdata+sdata)
        fidx += 1
        sidx += 1
    elif  fdatas[fidx][0] > sdatas[sidx][0] :
        sdata = sdatas[sidx][1]
        print "%d\t%d" % (sdatas[sidx][0],fdata+sdata)
        sidx += 1
    else:
        fdata = fdatas[fidx][1]
        print "%d\t%d" % (fdatas[fidx][0],fdata+sdata)
        fidx += 1

while fidx < len(fdatas):
    fdata = fdatas[fidx][1]
    print "%d\t%d" % (fdatas[fidx][0],fdata+sdata)
    fidx += 1

while sidx < len(sdatas):
    sdata = sdatas[sidx][1]
    print "%d\t%d" % (sdatas[sidx][0],fdata+sdata)
    sidx += 1
