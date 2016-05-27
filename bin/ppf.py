import os,sys
from datetime import datetime
import math
#Param
WINDOW=60
DELT=3

MINPOWERDIFF=20

keys=('waterheater2:basement', 'l004:kitchen', 'dishwasher:kitchen', 'l021:upstairs',
      'l012:nursery', 'oven:kitchen', 'humidifier1:upstairs', 'uptoilet:upstairs',
      'kitchensink:kitchen', 'l011:bedroom', 'microwave:kitchen', 'l002:kitchen',
      'shower:bathroom', 'downtoilet:bathroom', 'l009:diningroom', 'upsink:upstairs', 'l010:hallway',
      'hairdryer:bathroom', 'l005:kitchen', 'l013:mudroom', 'disposal:kitchen', 'washingmachine:basement',
      'l019:kitchen', 'l018:livingroom', 'toaster:kitchen', 'downsink:bathroom', 'l007:bathroom', 'l014:livingroom',
      'heatingindoorunit:house', 'fridge:kitchen', 'l006:kitchen', 'dryer:basement', 'heatingoutdoorunit:house')

class Node:
    def __init__(self,t):
        self.pre=self.next=None
        self.t=t

class SameNode(Exception):
    def __init__(self,node):
        self.node = node

class PowerNode(Node):
    def __init__(self,t,power):
        Node.__init__(self,t)
        self.power=power

# t, time
# device: 2d-array, 1st: open, 2nd: close
class DevicesNode(Node):
    def __init__(self,t,device,status=True):
        Node.__init__(self,t)
        self.devices=[[],[]]
        if status : self.devices[0] = [device]
        else: self.devices[1] = [device]
    def findData(self,plist):
        if self.pre is None or self.next is None : return None
        if len(self.devices[0]) + len(self.devices[1]) != 1 : return None

        prt=plist.head
        rhead=None
        while prt is not None:
            if prt.t >= self.t - WINDOW :
                rhead = prt
                break
            prt = prt.next
        if rhead is None or rhead.t >= self.t + WINDOW or rhead.t < self.pre.t + WINDOW : return None

        while prt is not None and prt.t <= self.t + WINDOW :
            prt = prt.next
        if prt is None : return None
        rtail = prt.pre
        if rtail == rhead or rtail.t > self.next.t - WINDOW : return None

        return (rhead,rtail)

    def findiff(self,plist):
        result = self.findData(plist)
        if result is None : return None
        return result[1].power - result[0].power

class List:
    def __init__(self):
        self.head=None
        self.tail=None
        self.size=0
    def add(self,node):
        if self.head is None :
            self.head = self.tail = node
            self.size = 1
            return
        pprt = None
        prt = self.head
        while prt is not None:
            if prt.t == node.t :
                raise SameNode(prt)
            if node.t < prt.t :
                if pprt : pprt.next = node
                else : self.head = node
                node.pre = pprt
                node.next = prt
                prt.pre = node
                self.size += 1
                return
            pprt = prt
            prt = prt.next
        pprt.next = node
        node.pre = pprt
        self.tail = node
        self.size += 1
    def addFromTail(self,node):
        if self.head is None :
            self.head = self.tail = node
            self.size = 1
            return
        pprt = None
        prt = self.tail
        while prt is not None:
            if prt.t == node.t :
                raise SameNode(prt)
            if node.t > prt.t :
                if pprt : pprt.pre = node
                else : self.tail = node
                node.pre = prt
                node.next = pprt
                prt.next = node
                self.size += 1
                return
            pprt = prt
            prt = prt.pre
        pprt.pre = node
        node.next = pprt
        self.head = node
        self.size += 1
    def find(self,t):
        prt = pprt = self.head
        while prt is not None:
            if prt.t == t : return prt
            if prt.t > t : return pprt
            pprt = prt
            prt = prt.next
        return pprt

class PowerList(List):
    def __init__(self,win=WINDOW,delt=DELT):
        List.__init__(self)
        self.win=win
        self.delt=delt
    def addPower(self,t,power):
        self.addFromTail(PowerNode(t,power))
    def find_diffs(self,t,win=None):
        prt=self.head
        frm=None
        dt = self.delt
        while prt is not Node :
            if prt.t > t : break
            _dt = t - prt.t
            if _dt <= dt:
                dt = _dt
                frm = prt
        if frm is None : return None
        if win is None or win > self.win : win = self.win

        diff=None
        while prt is not None and prt.next is not None:
            if prt.t < t :
                prt=prt.next
                continue
            if prt.t - t < self.win :
                diff=prt.next.power - prt.power
                if diff > MINPOWERDIFF : return diff
                elif diff < -MINPOWERDIFF : return diff
                else: diff = 0
            else:
                return diff
            prt=prt.next
        return diff

class DevicesStatusList(List):
    def addDevicesStatus(self,did,start,end):
        if end <= start : raise Exception("end must great than start")
        node = DevicesNode(start,did,True)
        try:
            self.addFromTail(node)
        except SameNode as snode:
            snode.node.devices[0].append(did)
        node = DevicesNode(end,did,False)
        try:
            self.addFromTail(node)
        except SameNode as snode:
            snode.node.devices[1].append(did)

# init Devices List
dlist = DevicesStatusList()

for line in open("ss.csv"):
    data=[int(x) for x in line.rstrip().split("\t")]
    if len(data) == 3:
        dlist.addDevicesStatus(data[2],data[0],data[1])

# init Power List
plist = PowerList()

for line in open("electric.csv"):
    data=[int(x) for x in line.rstrip().split("\t")]
    plist.addPower(*data)

print "-------------------------"
# first Time
node = dlist.head
pdevices={}

while node is not None:
    if node.t < plist.head.t :
        node=node.next
        continue
    if len(node.devices[0]) + len(node.devices[1]) == 1 :
        df = node.findiff(plist)
        if df is not None:
            print node.t,node.devices,df
            if len(node.devices[0]) == 1 :
                device = node.devices[0][0]
            else:
                device = node.devices[1][0]
            if device not in pdevices:
                pdevices[device] = [df]
            else:
                pdevices[device].append(df)
    node = node.next

for device in pdevices:
    print device,keys[device],pdevices[device]