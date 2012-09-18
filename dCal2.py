import pylab as p
import numpy as np
import csv
import tCal

with open('dCal') as f:
    H=[]
    for line in f:
        H.append(int(line.split()[1]))
        if len(H)==8190:
            break

n=200
ts=np.linspace(0,50,n+1)
N=[sum(H[j] for j in range(len(H)) if ts[i]<tCal.channelToTime(j)-6<ts[i+1]) for i in range(n)]
p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),[0]+reduce(lambda a,b:a+b,[[iN]*2 for iN in N])+[0])
p.show()
