__author__ = 'yaowei'
import os,sys
from datetime import datetime

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

frm='%Y-%m-%d %H:%M:%S'
basetime=datetime.strptime("2014-01-01 00:00:00",frm)
times=[]
min=0 # record from 0
COUNT=1500000
c=0
for line in open("../datas/exportedFromMatlab/study10electric1TimesStr.data"):
    if c < min :
        c += 1
        continue
    times.append(int((datetime.strptime(line[19:-1].replace("\t"," "),frm) - basetime).total_seconds()))
    if len(times) >= COUNT :
        break

values=[]
c=0
for line in open("../datas/exportedFromMatlab/study10electric1values.data"):
    if c < min :
        c += 1
        continue
    values.append(int(line.rstrip()))
    if len(values) >= COUNT:
        break
index = 0

c=0
for line in open("../datas/exportedFromMatlab/study10electric2values.data"):
    if c < min :
        c += 1
        continue
    values[index] += int(line.rstrip())
    index += 1
    if index >= COUNT: break

# for index in xrange(0,len(times)):
#     print "%d\t%d" % (times[index],values[index])

wtimes=[]
c=0
# for line in open("../datas/exportedFromMatlab/study10waterColdTimesStr.data"):
#     if c < min :
#         c += 1
#         continue
#     wtimes.append(int((datetime.strptime(line[19:-1].replace("\t"," "),frm) - basetime).total_seconds()))
#     if len(wtimes) >= COUNT :
#         break

cvalues=[]
c=0
old=None
w_factor=20000

# for line in open("../datas/exportedFromMatlab/study10waterColdvalues.data"):
#     if c < min :
#         c += 1
#         continue
#     # data = float(line.rstrip())
#     # if old is None :
#
#     cvalues.append(float(line.rstrip()) * w_factor)
#     if len(cvalues) >= COUNT:
#         break
# hvalues=[]
# c=0
# for line in open("../datas/exportedFromMatlab/study10waterHotvalues.data"):
#     if c < min :
#         c += 1
#         continue
#     hvalues.append(float(line.rstrip()) * w_factor)
#     if len(hvalues) >= COUNT:
#         break


dlist=[]
for line in open("ss.csv"):
    data=[ int(x) for x in line.rstrip().split("\t") ]
    if keys[data[2]] in ignores : continue
    dlist.append(data)

from pylab import *
plot(np.array(times),np.array(values))
# plot(np.array(wtimes),np.array(cvalues),color='g')
# plot(np.array(wtimes),np.array(hvalues),color='r')

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

def showValue(xdata):
    last = 0
    for idx in xrange(0,len(times)):
        if times[idx] >= xdata:
            break
        last = idx
    if xdata - times[last] < times[idx] - xdata : idx = last
    disps.append(annotate("%d,%d" % (times[idx],values[idx]),
        xy=(times[idx],values[idx]), xycoords='data',
        xytext=(times[idx],values[idx]+300), textcoords='data',
                    horizontalalignment="left",
                    arrowprops=dict(arrowstyle="simple",
                        connectionstyle="arc3,rad=-0.2"),
                    bbox=dict(boxstyle="round", facecolor="w",
                    edgecolor="0.5", alpha=0.9)
                ))
    # figure(1).canvas.draw()
    return (times[idx],values[idx])

def showDiff(event):
    WINDOW=20
    disps.append(plot([event.xdata-WINDOW,event.xdata-WINDOW],figure(1).axes[0].get_ylim(),'k--')[0])
    disps.append(plot([event.xdata+WINDOW,event.xdata+WINDOW],figure(1).axes[0].get_ylim(),'k--')[0])
    a = showValue(event.xdata-WINDOW)
    b = showValue(event.xdata+WINDOW)
    print a,b , b[0]-a[0],b[1]-a[1]

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
        showValue(event.xdata)
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
locations = [218032 ,
92477 ,
98603 ,
133719 ,
231444 ,
92476 ,
90474 ,
80673 ,
119103 ,
119104 ,
178579 ,
178580 ,
184261 ,
133984 ,
228729 ,
208847 ,
157694 ,
194472 ,
194471 ,
157693 ,
208848 ,
129548 ,
218031 ,
209852 ,
221324 ,
209853 ,
228465 ,
58539 ,
228466 ,
225064 ,
225065 ]
for item in locations[12:]:
    plot(times[item:item+25], values[item:item+25], color="grey", linewidth=2)
locations= [151277 ,
64011 ,
64012 ,
185310 ,
185311 ,
74174 ,
74175 ,
123695 ,
123696 ,
121265 ,
121266 ,
64171 ,
64172 ,
161009 ,
161010 ,
162445 ,
52674 ,
180311 ,
191001 ,
52675 ,
168309 ,
168308 ,
180312 ,
162446 ,
191002 ,
181316 ,
200964 ,
181315 ,
200965 ,
222064 ,
222065 ]
for item in locations[10:]:
    plot(times[item:item+25], values[item:item+25], color="pink", linewidth=2)

show()
