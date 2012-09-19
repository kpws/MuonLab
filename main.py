import pylab as p
import numpy as np
import csv
from tCal import timeToChannel, channelToTime

Hs=[]
ct=[channelToTime(i) for i in range(8190)]

for i in range(2):
    with open('muonAndPhoton'+['','2'][i]) as f:
        Hs.append([])
        for line in f:
            Hs[-1].append(int(line.split()[1]))
            if len(Hs[-1])==8190:
                break

n=200
ts=np.linspace(0,50,n+1)
#N=[sum(H[j] for j in range(len(H)) if ts[i]<ct[j]<ts[i+1]) for i in range(n)]
#p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),[0]+reduce(lambda a,b:a+b,[[iN]*2 for iN in N])+[0])
p.plot(np.sum(Hs,axis=0))
p.show()
