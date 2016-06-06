import os,sys

WINDOW=30
elec=[]

for line in open("electric.csv"):
    elec.append([ int(x) for x in line.rstrip().split("\t")])

starts=[]
closes=[]

for line in open("ss6.csv"):
    data = [ int(x) for x in line.rstrip().split("\t")]
    starts.append(data[0])
    closes.append(data[1])

idx = 1

for st in starts:
    datas=[]
    while elec[idx][0] <= st + WINDOW:
        if elec[idx][0] >= st - WINDOW:
            datas.append(idx)
        idx += 1
    if len(datas) < 2 :
        print "===" , st,"not Data"
        continue
    base = datas[0]
    print "===",st , " : "
    for d in datas[1:]:
        if elec[d][1]-elec[base][1] >= 100 :
            print "\t%d ++ %d" % ( elec[d][0] ,elec[d][1]-elec[base][1] )
        base = d




