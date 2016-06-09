
edatas=[]
WINDOW=30
DT= 2
for line in open("electric.csv"):
    edatas.append( [ int(x) for x in line.rstrip().split("\t") ] )

def getElectric(time,st=0,end=len(edatas)):
    if edatas[st][0] > time : return None

    for idx in xrange(st,end):
        if edatas[idx][0] >= time :
            break
    if idx == end : return None
    if time - edatas[idx-1][0] < edatas[idx][0] - time : idx -= 1
    if abs(time -edatas[idx][0]) > DT : return None
    return edatas[idx]

datas=[]
for line in open("ss.csv"):
    datas.append([ int(x) for x in line.rstrip().split("\t") ])

for idx in xrange(2,len(datas)-2):
    if datas[idx][2] == 32:
        for iidx in (-2,-1,1,2):
            if datas[iidx+idx][2] == 28:
                open,end = max(datas[idx][0],datas[iidx+idx][0]),min(datas[idx][1],datas[idx+iidx][1])
                openDt=(getElectric(open-WINDOW),getElectric(open+WINDOW))
                endDt=(getElectric(end-WINDOW),getElectric(end+WINDOW))
                print open,openDt , openDt[1][1]-openDt[0][1]
                print end,endDt , endDt[1][1]-endDt[0][1]

                break
        print "-"*30

