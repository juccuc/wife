#!/usr/bin/python

def readFileData(filename):
    datas=[]
    for line in open(filename):
        data = [int(x) for x in line.rstrip().split("\t")]
        datas.append(data)
    return datas

# hots=readFileData("../../datas/a/hot.2")
# colds=readFileData("../../datas/a/cold.2")

hot_colds = readFileData("../../datas/a/cold.hot.2")

start=None
end=None
result=[]
idx = 0
while idx < len(hot_colds):
    data = hot_colds[idx]
    if data[1] > 1920:
        if start is None :
            start = data
            for iidx in xrange(idx-1,0,-1):
                if hot_colds[iidx][1] == 0 :
                    start = hot_colds[iidx]
                if hot_colds[iidx][0] < hot_colds[idx][0] - 20 : break
        end = data
    elif end is not None:
        pidx = idx
        for iidx in xrange(idx,len(hot_colds)):
            if  hot_colds[iidx][0] > hot_colds[idx][0] + 20 : break
            if hot_colds[iidx][1] == 0 :
                pidx = iidx
                break
        data = hot_colds[pidx]
        if data[0] - start[0] > 10 :
            if len(result) > 0 and start[0] - result[-1][1][0]  < 15:
                result[-1][1] = data
            else:
                result.append([start,data])
        start = end = None
        idx = pidx
    idx += 1

idx = 0
while idx < len(result):
    data=result[idx]
    print data , data[1][0]-data[0][0] ,
    if idx > 0 :
        print data[0][0] - result[idx-1][1][0]
    else:
        print

    idx += 1