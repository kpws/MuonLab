from __future__ import division
import pylab as p
import numpy as np
import csv
from scipy.interpolate import interp1d

ts=[7,8,10,12,15,20,25,30,35,38,40,45,50]
lowCut=6.5
meanChannel=[]
stdChannel=[]
NChannel=[]
for t in ts:
    with open('tCalib/'+str(t)+'ns.txt') as csvFile:
        H=[]
        for line in csvFile:
            H.append(int(line.split()[1]))
            if len(H)==8190:
                break
        meanChannel.append(sum(H[i]*i for i in range(len(H))) / float(sum(H)))
        std=0
        for i in range(len(H)):
            std+=(i-meanChannel[-1])**2*H[i]
        std=np.sqrt(std/(sum(H)-1))
        stdChannel.append(std)
        NChannel.append(sum(H))
    if __name__ == "__main__":
        p.plot(H,label=str(t)+' ns')

errs=np.array(stdChannel)/np.sqrt(NChannel)
k,skit1,skit2,skit3=np.linalg.lstsq([np.array([ts[i],1]/errs[i]) for i in range(1,len(ts)-2)]  ,np.array(meanChannel[1:-2])/errs[1:-2])

def channelToTime(c):
    return (c-k[1])/k[0]

def timeToChannel(t):
    return k[1]+k[0]*t

if __name__ == "__main__":
    p.legend()
    p.figure()
    p.errorbar(ts,meanChannel,yerr=stdChannel)
    p.plot(np.linspace(ts[0],ts[-1],100),[timeToChannel(t) for t in np.linspace(ts[0],ts[-1],100)])
    p.show()
