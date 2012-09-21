import random
import numpy as np

h=1.2 #meter
d=2.4 #meter
v=3e8
c=3e8*0.9
n=1.5
maxTheta=np.arctan(h/d)


def getMuonTime():
    while True:
        x=random.random()*h
        theta=-maxTheta+2*random.random()*maxTheta
        x2=x+np.tan(theta)*d
        if 0<x2<h:
           return d/np.cos(theta)/v - d*np.tan(theta)/c*n



N=int(1e5)
t=[]
tb=[]
X=[]
Y=[]
p=0
for i in range(N):
    nP=i*100/N
    if nP!=p:
        p=nP
        print(str(p)+'%')
    tt=getMuonTime()
    t.append(tt)
print('100%')
import pylab as pl
pl.hist([it*1e9 for it in t], bins=200)
pl.xlabel('time [ns]')
#pl.figure()
#pl.hist([it*1e9 for it in tb], color='r', bins=200)
#pl.xlabel('time [ns]')
pl.show()
