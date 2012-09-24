import pylab as p
import numpy as np
import csv
from tCal import timeToChannel, channelToTime

Hs=[]
t=[channelToTime(i)*1e-9 for i in range(8190)]

for i in range(2):
    with open('muonAndPhoton'+['','2'][i]) as f:
        Hs.append([])
        for line in f:
            Hs[-1].append(int(line.split()[1]))
            if len(Hs[-1])==8190:
                break

H=np.sum(Hs,axis=0)

channelSize=[(t[i+1]-t[i-1])/2 for i in range(1,len(t)-1)]
channelSize=[channelSize[0]]+channelSize+[channelSize[-1]]
pdfPoints=[(0. if h!=h or h==float('inf') else h) for h in H/channelSize]
noiseT1=3.75e-8
noiseT2=3.99e-8
noise=np.mean([pdfPoints[i] for i in range(len(pdfPoints)) if noiseT1<t[i]<noiseT2])
pdfPoints=pdfPoints-noise
pdfPoints=[0]+pdfPoints/sum(pdfPoints*channelSize)+[0]
pdf=lambda it: np.interp(it, [t[0]-channelSize[0]]+t+[t[-1]+channelSize[-1]], [0]+list(pdfPoints)+[0])

if __name__=='__main__':
    #n=200
    #ts=np.linspace(0,50e-9,n+1)
    #N=[sum(H[j] for j in range(len(H)) if ts[i]<ct[j]<ts[i+1]) for i in range(n)]
    #p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),[0]+reduce(lambda a,b:a+b,[[iN]*2 for iN in N])+[0])
    pt=np.linspace(0,10e-8,1000)
    p.plot(pt,pdf(pt))
    p.show()
