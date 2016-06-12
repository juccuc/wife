def smooth(_datas,hold=0.1,winsize=3):
    fs = []
    indexes=[]
    store=None
    btw_hold = lambda x,y : x >= y - abs(y*hold) and x <= y + abs(y*hold)
    ave_func = lambda x,y : [(x[0]*x[1] + y[0]*y[1])/float(x[1]+y[1]),x[1]+y[1]]

    win=[]
    for index,data in _datas:
        indexes.append(index)
        if data > -10 and data < 10 :
            data = 0
        if store==None:
            store = [data,1]
        elif btw_hold(data,store[0]):
            store = ave_func(store,[data,1])
        else:
            if store[1] <= winsize :
                win.append(store)
            else:
                if len(win) > 0 :
                    for w in win:
                        store[1] += w[1]
                win=[]
                fs.append(map(int,store))
            store = [data,1]
    if store is not None:
        fs.append(map(int,store))
    results=[]
    index = 0
    for f in fs:
        if len(results) == 0 or f[0] != results[-1][1]:
            results.append((indexes[index],f[0]))
        index += f[1]
    return results

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
            if current[0] - 1 > result[-1][0] :
                result.append([current[0]-1,result[-1][1]])
            result.append(current)
    return result

datas=[]

for line in open("../electric.csv"):
    datas.append([int(x) for x in line.rstrip().split("\t")])

mdatas=smth_01(datas,120,20)

from pylab import *

zdatas=zip(*datas)
plot(zdatas[0],zdatas[1])
zdatas=zip(*mdatas)
plot(zdatas[0],zdatas[1],color="r")

show()
print datas[:20]
print mdatas[:20]