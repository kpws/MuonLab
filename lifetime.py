import pylab as p
import numpy as np
import csv
from tCal2 import timeToChannel, channelToTime
from scipy.optimize import newton
import random
def computeLifetime(h,time,tmin,tmax):
	Heff=[h[i] for i in range(len(h)) if tmax>time[i]>tmin]
	timeEff=[t for t in time if tmax>t>tmin]

	A=sum(timeEff[i]*Heff[i] for i in range(len(Heff)))
	B=sum(Heff)
	def lD(lambd):
		return B/lambd-A+B*(s1*np.exp(-s1*lambd)-s2*np.exp(-s2*lambd))/(np.exp(-s1*lambd)-np.exp(-s2*lambd))
	lambd=newton(lD,B/A)
	return sum(time[i]*h[i] for i in range(len(h)))/sum(h),1./lambd,B*np.log(lambd)-A*lambd-B*np.log(np.exp(-tmin*lambd)-np.exp(-tmax*lambd)),B
	
	
	


if __name__=="__main__":
	s1=2
	s2=15

	delay=0.004
	ct=[]
	with open('lifetime') as f:
		H=[]
		for line in f:
		    H.append(int(line.split()[1]))
		    ct.append(channelToTime(len(ct))-delay)
		    if len(H)==8190:
		        break

	n=200
	ts=np.linspace(0,50,n+1)
	N=[sum(H[j] for j in range(len(H)) if ts[i]<ct[j]<ts[i+1]) for i in range(n)]

	#p.figure()
	x=np.linspace(0.1,1,100)
	#p.plot(x,[lD(i) for i in x])
	lifetime1,lifetime,likelyhood,totalSamples=computeLifetime(H,ct,s1,s2)
	p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),[0]+reduce(lambda a,b:a+b,[[iN]*2 for iN in N])+[0],label="bins")
	p.plot(ct,H,label="raw")
	
	
	ensembleSize=50
	ensemblelifetime1=[0]*ensembleSize
	ensemblelifetime=[0]*ensembleSize
	ensembleLikelyhood=[0]*ensembleSize
	for i in range(ensembleSize):
		H=[0]*len(H)
		count=0
		while count<totalSamples*5:
			x=random.expovariate(1./lifetime)
			if s2>x>s1:
				count+=1
			H[int(timeToChannel(x)+0.5)]+=1
		ensemblelifetime1[i],ensemblelifetime[i],ensembleLikelyhood[i],t=computeLifetime(H,ct,s1,s2)
	
	p.plot(ct,H,label="sampled")
	p.legend(loc=1)
	p.figure()
	p.plot(ensemblelifetime1,'.',label="lifetime1")
	p.plot(ensemblelifetime,'.',label="lifetime")
	p.plot(ensembleSize/2,lifetime1,'.',label="True lifetime1")
	p.plot(ensembleSize/2,lifetime,'.',label="True lifetime")
	p.legend(loc=1)
	p.figure()
	p.plot(ensembleSize/2,likelyhood,'.',label="True likelyhood")
	p.plot(ensembleLikelyhood,'.',label="likelyhood")
	p.legend(loc=1)





	print lifetime
	print sum(ensemblelifetime)/ensembleSize
	print np.std(ensemblelifetime)
	p.show()











