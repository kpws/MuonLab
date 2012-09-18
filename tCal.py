import pylab as p
import numpy as np
import csv

ts=[8,9,10,11,12,13,14,16,18,20,30,40,50]
meanChannel=[]
for t in ts:
    with open('tCalib/'+str(t)+'ns.txt') as csvFile:
        H=[]
        for line in csvFile:
            H.append(int(line[13:].rstrip()))
            if len(H)==8190:
                break
        meanChannel.append(sum(H[i]*i for i in range(len(H))) / float(sum(H)))
    if __name__ == "__main__":
        p.plot(H,label=str(t)+' ns')

def channelToTime(c):
    return np.interp(c, meanChannel,ts)

if __name__ == "__main__":
    p.legend()
    p.figure()
    p.plot(meanChannel,channelToTime(meanChannel),'.-')
    p.show()

def timeToChannel(t):
    return np.interp(t, ts, meanChannel)
