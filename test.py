import random
import numpy as np

width=0.6 #meter
height=1.2 #meter
turnY=0.91 #meter
a=0.04  #meter
d=2.438 #meter
sourceY=0.4 #meter

c=3e8 #m/s
nScint=1.5
v=c*0.9
rate=1e4 #1/(m^2s)

maxTheta=np.arctan(np.sqrt(height**2+width**2)/d)
minCosTheta=(d/np.sqrt(height**2+width**2+d**2))**3

k=(width-a)/2/(height-turnY)
area=width*height-2*((width-a)/2*(height-turnY)/2)
lambd=area*rate
print 1/lambd*1e9
def inGeo(x, y):
    return 0<x<width and 0<y<height and x>k*(y-turnY) and x<width-k*(y-turnY)

def timeToPMT(x, y):
    return np.sqrt((x-width/2)**2+(y-height)**2)/(c/nScint)

def getMuonTime():
    while True:
        x=random.random()*width
        y=random.random()*height
        if not inGeo(x, y):
            continue
        phi=random.random()*2*np.pi
        cosTheta=(random.random()*(1-minCosTheta)+minCosTheta)**(1./3)
        x2=x+np.cos(phi)*d*np.sqrt(1-cosTheta**2)/cosTheta
        y2=y+np.sin(phi)*d*np.sqrt(1-cosTheta**2)/cosTheta#np.tan(theta)*d
        if inGeo(x2, y2):
            return d/cosTheta/v - timeToPMT(x, y) + timeToPMT(x2, y2)

def getPhotonTime():
    x2=width/2
    y2=sourceY
    while True:
        phi=random.random()*2*np.pi
        cosTheta=random.random()*(1-minCosTheta)+minCosTheta
        x1=x2-np.cos(phi)*d*np.sqrt(1-cosTheta**2)/cosTheta
        y1=y2-np.sin(phi)*d*np.sqrt(1-cosTheta**2)/cosTheta
        if inGeo(x1, y1):
           return -d/cosTheta/v - timeToPMT(x1, y1) + timeToPMT(x2, y2)


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
    if random.random()<0.5:
        tt=getPhotonTime()
    else:
        tt=getMuonTime()
    '''p1ot=random.expovariate(lambd)
    p2ot=random.expovariate(lambd)
    if p1ot<tt:
        if p2ot<tt:
            T=p2ot-p1ot
        else:
            T=tt-p1ot
    elif p2ot<tt:
        T=p2ot
    else:
        T=tt
    T=min(T,50e-9)

    if T>0:
        tb.append(T)'''
    t.append(tt)
print('100%')
import pylab as pl
pl.hist([it*1e9 for it in t], bins=200)
pl.xlabel('time [ns]')
#pl.figure()
#pl.hist([it*1e9 for it in tb], color='r', bins=200)
#pl.xlabel('time [ns]')
pl.show()
