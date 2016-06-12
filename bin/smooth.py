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
                tvalue += (cur[1] - result[-1][1]) * ( cur[0] - datas[iidx-1][0] )
                tsec += ( cur[0] - datas[iidx-1][0] )
            else:
                tvalue += (cur[1] - result[-1][1]) * ( current[0] + adhere - datas[iidx-1][0] )
                tsec += ( current[0] + adhere - datas[iidx-1][0] )
                break
        if tsec > 0 :
            cf = ( tvalue / tsec ) / (1.0 * diff)
            fit = cf >= 0.6 # and cf <= 1.1
        if fit :
            # if current[0] - 1 > result[-1][0] :
            #     result.append([current[0]-1,result[-1][1]])
            result.append(current)
    return result
def smth_02(datas,threshold=80,adhere=10):
    if datas is None or len(datas) == 0 : return None
    result=[datas[0]]
    idx = 1
    while idx < len(datas):
        current = datas[idx]
        diff=current[1] - result[-1][1]
        if abs(diff) < threshold :
            if abs(current[1]) < threshold/2 and result[-1][1] != 0 :
                result.append([current[0],0])
            idx += 1
            continue
        # change if diff can adhere to ($adhere) seconds
        fit=True
        tvalue=0
        tsec=0
        for iidx in xrange(idx+1,len(datas)):
            cur = datas[iidx]
            if cur[0] < current[0] + adhere :
                tvalue += (cur[1] + datas[iidx-1][1]) * ( cur[0] - datas[iidx-1][0] ) / 2
                tsec += ( cur[0] - datas[iidx-1][0] )
            else:
                c=current[0] + adhere - datas[iidx-1][0]
                d=cur[0] - datas[iidx-1][0] - c
                a=datas[iidx-1][1]
                b=cur[1]
                tvalue += ( (a*d + b*c)/(c+d) + a ) * c / 2
                tsec += c
                break
        if tsec > 0 :
            value = tvalue / tsec
            if abs(value - result[-1][1]) >= threshold :
                result.append([current[0],value])
            if datas[iidx][0] <= current[0] + adhere :
                idx = iidx + 1
            else:
                idx = iidx
        else:
            result.append(current)
            idx += 1
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
parser.add_argument("--fnum",type=int,choices=[1,2],default=2)
parser.parse_args()

args=parser.parse_args()

#----------------------

if not os.path.isfile(args.input) :
    print "File",args.input ,"is not exists"
    sys.exit(1)

source=readFileData(args.input)
# func = "smth_%02d" % args.fnum

funcc= [
    smth_01,smth_02
]
destine=funcc[args.fnum-1](source,args.threshold,args.adhere)

for data in destine :
    print "%d\t%d" % tuple(data)

