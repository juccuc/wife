#!/usr/bin/python

import argparse
import os,sys

def smth_01(datas,threshold=80,adhere=10):
    if datas is None or len(datas) == 0 : return None
    result=[datas[0]]

    for idx in xrange(1,len(datas)):
        current = datas[idx]
        diff=current[1] - result[-1][1]
        if abs(diff) < threshold : continue
        # change if diff can adhere to ($adhere) seconds
        fit=True
        tvalue=0
        tsec=0
        for iidx in xrange(idx+1,len(datas)):
            cur = datas[iidx]
            if cur[0] < current[0] + adhere :
                tvalue += cur[1] * ( cur[0] - datas[iidx-1][0] )
                tsec += ( cur[0] - datas[iidx-1][0] )
            else:
                tvalue += cur[1] * ( current[0] + adhere - datas[iidx-1][0] )
                tsec += ( current[0] + adhere - datas[iidx-1][0] )
                break
        if tsec > 0 :
            cf = ( tvalue / tsec - result[-1][1]) / (1.0 * diff)
            fit = cf >= 0.9 and cf <= 1.1
        if fit :
            # if current[0] - 1 > result[-1][0] :
            #     result.append([current[0]-1,result[-1][1]])
            result.append(current)
    return result
def readFileData(filename):
    datas=[]
    for line in open(filename):
        datas.append([int(x) for x in line.rstrip().split("\t")])
    return datas

# ---- parameter ------
parser = argparse.ArgumentParser()
parser.add_argument("input",help="Data's file")
parser.add_argument("--threshold",type=int , default=80)
parser.add_argument("--adhere",type=int , default=10)
parser.parse_args()

args=parser.parse_args()

#----------------------

if not os.path.isfile(args.input) :
    print "File",args.input ,"is not exists"
    sys.exit(1)

source=readFileData(args.input)
destine=smth_01(source,args.threshold,args.adhere)

for data in destine :
    print "%d\t%d" % tuple(data)

