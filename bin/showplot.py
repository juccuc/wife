import os,sys
from datetime import datetime
from pylab import *

# ----- static datas -----------
keys=('waterheater2:basement', 'l004:kitchen', 'dishwasher:kitchen', 'l021:upstairs',
      'l012:nursery', 'oven:kitchen', 'humidifier1:upstairs', 'uptoilet:upstairs',
      'kitchensink:kitchen', 'l011:bedroom', 'microwave:kitchen', 'l002:kitchen',
      'shower:bathroom', 'downtoilet:bathroom', 'l009:diningroom', 'upsink:upstairs', 'l010:hallway',
      'hairdryer:bathroom', 'l005:kitchen', 'l013:mudroom', 'disposal:kitchen', 'washingmachine:basement',
      'l019:kitchen', 'l018:livingroom', 'toaster:kitchen', 'downsink:bathroom', 'l007:bathroom', 'l014:livingroom',
      'heatingindoorunit:house', 'fridge:kitchen', 'l006:kitchen', 'dryer:basement', 'heatingoutdoorunit:house')
ignores = (
#    'uptoilet:upstairs','shower:bathroom','downtoilet:bathroom','upsink:upstairs','downsink:bathroom','fridge:kitchen',
)
START=0 # record from 0
COUNT=150000000

# ---------------------------------

# -------- function ---------------
def readFileData(filename,start=0,count=-1):
    datas=[]
    DT = 3
    for line in open(filename):
        if start > 0 :
            start -= 1
            continue
        count -= 1
        if count == 0 : break
        data = [int(x) for x in line.rstrip().split("\t")]
        if len(datas) > 0 and data[0] > datas[-1][0] + DT and data[1] != datas[-1][1] :
            datas.append([data[0] - DT , datas[-1][1]])
        datas.append(data)
    return datas
def showPlot(data,**kwargs) :
    datas = zip(*data)
    plot(datas[0],datas[1],**kwargs)
    

edatas=readFileData("../datas/a/electric01",START,COUNT)
hdatas=readFileData("../datas/a/hot.2",START,COUNT)
cdatas=readFileData("../datas/a/cold.2",START,COUNT)

showPlot(edatas,color="purple")
showPlot(cdatas,color="blue")
showPlot(hdatas,color="r")

dlist=[]
for line in open("ss.csv"):
    data=[ int(x) for x in line.rstrip().split("\t") ]
    if keys[data[2]] in ignores : continue
    dlist.append(data)

disps=[]

dr_datas={}
def draw_dr_datas(event=None):
    if len(dr_datas) > 0 :
        vv=figure(1).axes[0].get_ylim()
        dy=(vv[1]-vv[0])/(len(dr_datas) + 1)
        y=dy + vv[0]
        for key in dr_datas:
            for data in dr_datas[key]:
                disps.append(plot([data[0],data[1]],[y,y],'k-')[0])
                disps.append(plot([data[0],data[0]],vv,'k--')[0])
                disps.append(plot([data[1],data[1]],vv,'k--')[0])
                disps.append(annotate(keys[key],
                    xy=(event.xdata,y), xycoords='data',
                    xytext=(event.xdata,y+dy/3), textcoords='data',
                    horizontalalignment="left",
                    arrowprops=dict(arrowstyle="simple",
                        connectionstyle="arc3,rad=-0.2"),
                    bbox=dict(boxstyle="round", facecolor="w",
                    edgecolor="0.5", alpha=0.9)
                ))
            y += dy
    figure(1).canvas.draw()

def draw(event):
    global  disps,dr_datas
    fig = figure(1)
    vv=fig.axes[0].get_ylim()
    # print vv
    disps.append(plot([event.xdata,event.xdata],vv,'k-',color="r")[0])

    for indx in xrange(0,len(dlist)):
        if event.xdata >= dlist[indx][0] and event.xdata <= dlist[indx][1] :
            if dr_datas.has_key(dlist[indx][2]):
                dr_datas[dlist[indx][2]].add((dlist[indx][0],dlist[indx][1]))
            else:
                dr_datas[dlist[indx][2]] = set([(dlist[indx][0],dlist[indx][1])])

        if event.xdata < dlist[indx][0] : break
    draw_dr_datas(event)

# figure(1).canvas.mpl_connect('button_press_event',onClick)
def removeAll(event=None):
    global  disps,dr_datas
    for play in disps :
        play.remove()
    disps=[]
    figure(1).canvas.draw()

def showValue(xdata,datas):
    last = 0
    for idx in xrange(0,len(datas)):
        if datas[idx][0] >= xdata:
            break
        last = idx
    if xdata - datas[last][0] < datas[idx][0] - xdata : idx = last
    disps.append(annotate("%d,%d" % (datas[idx][0],datas[idx][1]),
        xy=(datas[idx][0],datas[idx][1]), xycoords='data',
        xytext=(datas[idx][0],datas[idx][1]+300), textcoords='data',
                    horizontalalignment="left",
                    arrowprops=dict(arrowstyle="simple",
                        connectionstyle="arc3,rad=-0.2"),
                    bbox=dict(boxstyle="round", facecolor="w",
                    edgecolor="0.5", alpha=0.9)
                ))
    # figure(1).canvas.draw()
    return datas[idx]

def showDiff(event):
    WINDOW=20
    disps.append(plot([event.xdata-WINDOW,event.xdata-WINDOW],figure(1).axes[0].get_ylim(),'k--')[0])
    disps.append(plot([event.xdata+WINDOW,event.xdata+WINDOW],figure(1).axes[0].get_ylim(),'k--')[0])
    a = showValue(event.xdata-WINDOW,hdatas)
    b = showValue(event.xdata+WINDOW,hdatas)
    print "hot water:" ,a,b , b[0]-a[0],b[1]-a[1]

    a = showValue(event.xdata-WINDOW,cdatas)
    b = showValue(event.xdata+WINDOW,cdatas)
    print "cold water:" ,a,b , b[0]-a[0],b[1]-a[1]

def onPress(event):
    global dr_datas
    if event.key == 'x':
        removeAll(event)
        dr_datas={}
        return
    if event.key == 'd':
        removeAll(event)
        draw(event)
        return
    if event.key == 'q':
        disps.append(plot([event.xdata,event.xdata],figure(1).axes[0].get_ylim(),'k--')[0])
        figure(1).canvas.draw()
        return
    if event.key == 'w':
        disps.append(plot(figure(1).axes[0].get_xlim(),[event.ydata,event.ydata],'k--')[0])
        figure(1).canvas.draw()
        return
    if event.key == 'e':
        disps.append(plot([event.xdata,event.xdata],figure(1).axes[0].get_ylim(),'k--')[0])
        disps.append(plot(figure(1).axes[0].get_xlim(),[event.ydata,event.ydata],'k--')[0])
        figure(1).canvas.draw()
        return
    if event.key == 'f':
        showValue(event.xdata,hdatas)
        figure(1).canvas.draw()
        return
    if event.key == 'g':
        showValue(event.xdata,cdatas)
        figure(1).canvas.draw()
        return
    if event.key == 'a':
        showDiff(event)
        figure(1).canvas.draw()
        return
figure(1).canvas.mpl_connect('key_press_event',onPress)

# opens=[]
# closes=[]
# values=[]
# texts=[]
# for line in open("ss.csv"):
#     data=line.rstrip().split("\t")
#     st=int(data[0])
#     ed=int(data[1])
#     idx=int(data[2])
#     if keys[idx] in ignores : continue
#     if st < times[0] and ed < times[0] : continue
#     if st > times[-1] and ed > times[0] :
#         continue
#     plot([st,ed],[500+idx*500,500+idx*500],'k-')
#     plot([st,st],[2000,16000],'k--')
#     plot([ed,ed],[2000,16000],'k--')
#
#     opens.append(st)
#     values.append(500+idx*500)
#     closes.append(ed)
#     texts.append(idx)
# # plot(opens,values,marker='+',color='r',ls='')
# # plot(closes,values,marker='x',color='r',ls='')
#
#
# for idx in texts:
#     text(times[0]-10000,idx*500+500,keys[idx])

show()
