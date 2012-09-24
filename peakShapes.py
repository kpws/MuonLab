import random
import numpy as np
import csv
import pylab as pl

steps=80
err=0.01

width=0.6 #meter
height=1.2 #meter
turnY=0.91 #meter
a=0.04  #meter
d=2.438 #meter
sourceY=0.35 #0.4 #meter

c=3e8#2.99792458e8 #m/s
nScint=1.5
vs=np.linspace(0.5,1,30)*c
rate=1e4 #1/(m^2s)

maxTheta=np.arctan(np.sqrt(height**2+width**2)/d)
minCosTheta=d/np.sqrt(height**2+width**2+d**2)

k=(width-a)/2/(height-turnY)
area=width*height-2*((width-a)/2*(height-turnY)/2)
lambd=area*rate

def inGeo(x, y):
    return 0<x<width and 0<y<height and x>k*(y-turnY) and x<width-k*(y-turnY)

def timeToPMT(x, y):
    return np.sqrt((x-width/2)**2+(y-height)**2)/(c/nScint)

def getMuonTime(v):
    while True:
        x1=random.random()*width
        y1=random.random()*height
        if not inGeo(x1, y1):
            continue
        phi=random.random()*2*np.pi
        cosTheta=random.random()*(1-minCosTheta)+minCosTheta
        x2=x1+np.cos(phi)*d*np.sqrt(1-cosTheta**2)/cosTheta
        y2=y1+np.sin(phi)*d*np.sqrt(1-cosTheta**2)/cosTheta#np.tan(theta)*d
        if inGeo(x2, y2):
            return d/cosTheta/v - timeToPMT(x1, y1) + timeToPMT(x2, y2)


def getPhotonTime():
    x2=width/2
    y2=sourceY
    while True:
        phi=random.random()*2*np.pi
        cosTheta=random.random()*(1-minCosTheta)+minCosTheta
        x1=x2-np.cos(phi)*d*np.sqrt(1-cosTheta**2)/cosTheta
        y1=y2-np.sin(phi)*d*np.sqrt(1-cosTheta**2)/cosTheta
        if inGeo(x1, y1):
           return -d/cosTheta/c - timeToPMT(x1, y1) + timeToPMT(x2, y2)

muonT=dict()
muonF=dict()
for typ in ['muon','photon']:
    try :
        for v in (vs if typ=='muon' else ['']):
            r=csv.reader(open(typ+str(v)+'TimeMC','r'), delimiter='\t')
            if typ=='muon':
                z=zip(*[ir for ir in r])
                muonT[v],muonF[v]=(map(float,z[0]),map(float,z[1]))
            else:
                z=zip(*[ir for ir in r])
                photonT,photonF=(map(float,z[0]),map(float,z[1]))
    except IOError:
        N=int((1/err)**2*steps+1)
        for v in (vs if typ=='muon' else ['']):
            t=[]
            p=0
            for i in range(N):
                nP=i*100/N
                if nP!=p:
                    p=nP
                    print(str(p)+'%')
                if typ=='photon':
                    tt=getPhotonTime()
                else:
                    tt=getMuonTime(v)
                t.append(tt)
            print('100%')
            ts=np.linspace(min(t), max(t), steps+1)
            T=np.linspace((ts[0]+ts[1])/2, (ts[-2]+ts[-1])/2, steps)
            F=[float(sum(1 for it in t if ts[i]<it<ts[i+1]))/N/(ts[1]-ts[0]) for i in range(steps)]
            f=open(typ+str(v)+'TimeMC','w')
            for i in range(steps):
                f.write(str(T[i])+'\t'+str(F[i])+'\n')
            if typ=='muon':
                muonT[v]=T
                muonF[v]=F
            else:
                photonT=T
                photonF=F

muonPDF=lambda t,v: np.array([np.interp(v,vs,[np.interp(it,
            [muonT[iv][0]-(muonT[iv][1]-muonT[iv][0])/2]+muonT[iv]+[muonT[iv][-1]+(muonT[iv][1]-muonT[iv][0])/2],
            [0]+muonF[iv]+[0]) for iv in vs]) for it in t])

photonPDF=lambda t: np.interp(t,
            [photonT[0]-(photonT[1]-photonT[0])/2]+photonT+[photonT[-1]+(photonT[1]-photonT[0])/2],
            [0]+photonF+[0])

if __name__=='__main__':
    for v in vs:
        pl.plot(muonT[v],muonF[v])
    pl.plot(photonT,photonF)
    pl.show()
