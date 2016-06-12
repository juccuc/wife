from pylab import *

datas=[]
df = None
MIN=80
GT=5
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

class Device:
    def __init__(self,name,power,std,dur=5):
        self.name = name
        self.power = power
        self.std = std
        self.dur = dur
        self.status = -1        # -1 unknow 0 close 1 open
    def validDf(self,idx):
        global dfs

        base=idx
        df=dfs[idx]
        df_t = df[2]-df[0]
        df_v = df[3]-df[1]

        ret=0
        minDT=self.std

        while True :
            if df_t > self.dur : break
            if df_v <= -self.power + self.std and df_v >= -self.power - self.std :
                if ret == 0 or abs(df_v + self.power) < minDT :
                    ret = -(idx - base + 1)
                    minDT = abs(df_v + self.power)
            if df_v <= self.power + self.std and df_v >= self.power - self.std :
                if ret == 0 or abs(df_v - self.power) < minDT :
                    ret = idx-base+1
                    minDT = abs(df_v - self.power)
            idx += 1
            if idx >= len(dfs) : break
            ndf = dfs[idx]
            df_t = ndf[2] - df[0]
            df_v = ndf[3] - df[1]
        return ret

class Dryer(Device):
    def __init__(self,name) :
        Device.__init__(self,name,(4882,),(43,),durations=(2,15))

    def validDf(self,df):
        pass

devices= (
    Device("HeatingIndoor",10206,1500,60),
    Device("Microwave",1681,52,10),
    Device("Humidifier",1470,112,10),
    Device("Waterheater",4391,504),
)

dfs = []
times=[]
values=[]
for line in open("../electric.csv"):
    datas.append([ int(x) for x in line.rstrip().split("\t") ])
    times.append(datas[-1][0])
    values.append(datas[-1][1])
    if len(datas) > 1 :
        if datas[-1][0] - datas[-2][0] <= GT and abs(datas[-1][1] - datas[-2][1]) > 80:
            if df is not None:
                df[2],df[3] = datas[-1]
            else:
                df = [datas[-2][0],datas[-2][1],datas[-1][0],datas[-1][1]]
        elif df is not None:
            if abs(df[3]-df[1]) > 80:
                dfs.append(df)
            df=None
idx = 0
adds_lines = [
    # (3542411,-1,0,12644) , (3585032,-1,0,11008)
]
for line in adds_lines:
    plot([line[0],line[0]+line[1]],[line[3],line[3] + line[1] * devices[line[2]].power],'k-',color="r",linewidth=5)

mdatas = [[]] * len(devices)

while idx < len(dfs):
    for index,device in enumerate(devices):
        ret=device.validDf(idx)
        if ret != 0 :
            mdatas[index].append((idx,ret))
            if index == 1 :
                print dfs[idx:idx+abs(ret)],ret,device.name
                if ret > 0 :
                    plot([dfs[idx][0],dfs[idx+abs(ret)-1][2]],[dfs[idx][1],dfs[idx+abs(ret)-1][3]],'k-',color="r",linewidth=5)
                else:
                    plot([dfs[idx][0],dfs[idx+abs(ret)-1][2]],[dfs[idx][1],dfs[idx+abs(ret)-1][3]],'k-',color="yellow",linewidth=5)
            idx += abs(ret) - 1
            break
    idx += 1

# figure(2)
# mtimes=[]
# mvalues=[]
# for mdata in mdatas[0]:

dlist=[]
for line in open("../ss.csv"):
    data=[ int(x) for x in line.rstrip().split("\t") ]
    if keys[data[2]] in ignores : continue
    dlist.append(data)

plot(np.array(times),np.array(values))

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
    xlim=figure(1).axes[0].get_xlim()
    ylim=figure(1).axes[0].get_ylim()
    WINDOW=(xlim[1]-xlim[0])/10
    disps.append(plot([event.xdata-WINDOW,event.xdata-WINDOW],ylim,'k--')[0])
    disps.append(plot([event.xdata+WINDOW,event.xdata+WINDOW],ylim,'k--')[0])
    a = showValue(event.xdata-WINDOW)
    b = showValue(event.xdata+WINDOW)
    # disps.append(annotate("%d,%d" % (times[idx],values[idx]),
    #     xy=(times[idx],values[idx]), xycoords='data',
    #     xytext=(times[idx],values[idx]+300), textcoords='data',
    #                 horizontalalignment="left",
    #                 arrowprops=dict(arrowstyle="simple",
    #                     connectionstyle="arc3,rad=-0.2"),
    #                 bbox=dict(boxstyle="round", facecolor="w",
    #                 edgecolor="0.5", alpha=0.9)
    #             ))
    bbox_props = dict(boxstyle="round,pad=0.3", fc="cyan", ec="b", lw=2)
    disps.append(text(event.xdata, event.ydata, "%d - %d" % (b[0]-a[0],b[1]-a[1]), ha="center", va="center",
                size=12,
                bbox=bbox_props))
    print a,b , b[0]-a[0],b[1]-a[1]

def removeAll(event=None):
    global  disps,dr_datas
    for play in disps :
        play.remove()
    disps=[]
    dr_datas={}
    figure(1).canvas.draw()

def onPress(event):
    global dr_datas
    if event.key == 'x':
        removeAll(event)
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

show()
