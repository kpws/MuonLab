from peakShapes import photonPDF, muonPDF
import speedExp
import pylab as pl
import numpy as np
from scipy import trapz
from scipy.optimize import fmin

c=2.99792458e8

t=np.linspace(-40e-9,40e-9,2500)
pl.plot(t, speedExp.pdf(t),'k',label='Experimental')

t1=6.6e-9
t2=1.66e-8
t3=3.6e-8

#for x in [t1,t2,t3]:
#    pl.plot([x]*2,[0,1e8],'-k')

#dt=how much p2 is delayed compared to p1
def err1(dt,I):
    t=np.linspace(t1,t2,1000)
    return sum((photonPDF(t-dt)*I-speedExp.pdf(t))**2)

def err2(v,I):
    t=np.linspace(t2,t3,1000)
    return sum((muonPDF(t-dt,v)*I-speedExp.pdf(t))**2)


t=np.linspace(t1,t2,1000)
#I1=sum(speedExp.pdf(t))*(t[1]-t[0])
x=fmin(lambda x:err1(x[0]*1e-9,x[1])*1e-14,[17,0.05])
dt=x[0]*1e-9
I1=x[1]
t=np.linspace(t2,t3,100)
#I2=sum(speedExp.pdf(t))*(t[1]-t[0])
x=fmin(lambda x:err2(x[0]*c,x[1])*1e-14,[0.8,1.])
v=x[0]*c
print v
I2=x[1]
#dts=np.linspace(0,30,500)
#pl.figure()
#pl.plot(dts,[err(dt*1e-9,x[1]) for dt in dts])

t=np.linspace(t1,t2,1000)
pl.plot(t,photonPDF(t-dt)*I1,label='Fit of Monte-Carlo data for photons',color='r')
t=np.linspace(t2,t3,1000)
pl.plot(t,muonPDF(t-dt,v)*I2,label='Fit of Monte-Carlo data for muons',color='b')
#for v in np.linspace(0.5,1,5)*c:
#   pl.plot(t,muonPDF(t,c))
pl.legend(loc=2)
pl.axis([0.5e-8,3.8e-8,0,2.5e8])
pl.xlabel('TAC time, [s]')
pl.ylabel('Probability density, [s$^{-1}$]')
pl.savefig('speedFit.pdf',bbox_inches=0)
pl.show()
