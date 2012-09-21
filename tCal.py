from __future__ import division
import pylab as p
import numpy as np
import csv

ts=[7,8,10,12,15,20,25,30,35,38,40,45,50]
lowCut=6.5
meanChannel=[]
stdChannel=[]
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
    if __name__ == "__main__":
        p.plot(H,label=str(t)+' ns')

def channelToTime(c):
    if c<meanChannel[0]:
        return max(lowCut, (c-meanChannel[0])/(meanChannel[1]-meanChannel[0])*(ts[1]-ts[0])+ts[0])
    else:
        return np.interp(c, meanChannel,ts)

def timeToChannel(t):
    if t<ts[0]:
        return (max(t, lowCut)-ts[0])/(ts[1]-ts[0])*(meanChannel[1]-meanChannel[0])+meanChannel[0]

    return np.interp(t, ts, meanChannel)

if __name__ == "__main__":
    p.legend()
    p.figure()
    print stdChannel
    p.errorbar(ts,meanChannel,yerr=stdChannel)
    p.show()
