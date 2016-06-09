#!/usr/bin/python
import os,sys
import utils

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

if __name__ == "__main__":
	if len(sys.argv) != 5:
		utils.printUsage(("datafile","threshold","winsize","outputfile"))
	results = smooth(utils.readData(sys.argv[1],int),float(sys.argv[2]),int(sys.argv[3]))
	utils.writeData(sys.argv[4],results,'%d\t%d\n')
