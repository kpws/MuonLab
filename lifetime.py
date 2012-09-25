import pylab as p
import numpy as np
import csv
from tCal2 import timeToChannel, channelToTime
from scipy.optimize import newton,fmin
import random
import sys
def computeLifetime(h,time,tmin,tmax):
	Heff=[h[i] for i in range(len(h)) if tmax>time[i]>tmin]
	timeEff=[t for t in time if tmax>t>tmin]
	
	A=sum(timeEff[i]*Heff[i] for i in range(len(Heff)))
	B=sum(Heff)
	def l(lambdac):
		lambd=1./lambdac[0]
		lambd2=1./lambdac[2]
		c=lambdac[1]
#		A=lambdac[3]**2
#		c=np.sqrt(0.0015)
		A=0.5		
		#print lambdac
		return -sum(Heff[i]*(np.log(A*np.exp(-lambd*timeEff[i])+(1-A)*np.exp(-lambd2*timeEff[i])+c**2)-np.log(
		(A*(np.exp(-lambd*tmin)-np.exp(-lambd*tmax))/lambd+(1-A)*(np.exp(-lambd2*tmin)-np.exp(-lambd2*tmax))/lambd2 + c**2*(tmax-tmin)))) for i in range(len(Heff)))

	def lD(lambd):
		return B/lambd-A+B*(s1*np.exp(-s1*lambd)-s2*np.exp(-s2*lambd))/(np.exp(-s1*lambd)-np.exp(-s2*lambd))
	lambd=newton(lD,B/A)
	val=fmin(l,[2.2,0.001,1.7])
	print 1./lambd
	print val
	lambd=1./val[0]
#	print "asdf"

	return sum(time[i]*h[i] for i in range(len(h)))/sum(h),1./lambd,B*np.log(lambd)-A*lambd-B*np.log(np.exp(-tmin*lambd)-np.exp(-tmax*lambd)),B,val[1]
	
	
	


if __name__=="__main__":
	s1=2
	s2=15

	delay=0.004
	ct=[]
	with open('lifetimeFinal') as f:
		H=[]
		for line in f:
		    H.append(int(line.split()[1]))
		    ct.append(channelToTime(len(ct))-delay)
		    if len(H)==8190:
		        break

	n=100
	ts=np.linspace(0,50,n+1)
	N=[sum(H[j] for j in range(len(H)) if ts[i]<ct[j]<ts[i+1]) for i in range(n)]

	#p.figure()
	x=np.linspace(0.1,1,100)
	#p.plot(x,[lD(i) for i in x])
	lifetime1,lifetime,likelyhood,totalSamples,c=computeLifetime(H,ct,s1,s2)
	print totalSamples
	p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),[0]+reduce(lambda a,b:a+b,[[float(iN)/totalSamples/ts[1]]*2 for iN in N])+[0],label="Data")
	p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),1./lifetime/(np.exp(-s1/lifetime)-np.exp(-s2/lifetime)+c**2*(s2-s1))*(np.exp(reduce(lambda a,b:a+b,[[t]*2 for t in ts])/(-lifetime))+c**2),label="Fit")
	p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),1./lifetime/(np.exp(-s1/lifetime)-np.exp(-s2/lifetime)+c**2*(s2-s1))*np.ones(2*len(ts))*c**2)
	p.show()
#	p.plot(ct,H,label="raw")
	noisePoints=1./(c**2/(np.exp(-s1/lifetime)*lifetime-np.exp(-s2/lifetime)*lifetime+c**2*(s2-s1)))
	print noisePoints
	noisePoints_t=noisePoints
#	noisePoints=1./noisePoints*totalSamples

	ensembleSize=20
	ensemblelifetime1=[0]*ensembleSize
	ensemblelifetime=[0]*ensembleSize
	ensembleLikelyhood=[0]*ensembleSize
	noise=[]
	for i in range(ensembleSize):
		print i
		H=[0]*len(H)
		HN=[0]*len(H)
		count=0
		noisePoints_t=noisePoints
		while count<totalSamples:
			x=random.expovariate(1./2.1)
	#		if count>noisePoints_t:
	#			x=random.random()*(s2-s1)+s1
	 #                       HN[int(timeToChannel(x)+0.5)]+=1
	#			noisePoints_t+=noisePoints

			if s2>x>s1:
				count+=1
			H[int(timeToChannel(x)+0.5)]+=1


#		for j in range(len(H)):
#			H[j]=H[j]+noisePoints*1./(timeToChannel(s2)-timeToChannel(s1))
		ensemblelifetime1[i],ensemblelifetime[i],ensembleLikelyhood[i],t,t2=computeLifetime(H,ct,s1,s2)
		noise.append(t2**2/(np.exp(-s1/ensemblelifetime[i])*ensemblelifetime[i]-np.exp(-s2/ensemblelifetime[i])*ensemblelifetime[i]+t2**2*(s2-s1))*(s2-s1))
		print count
	
	p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),[0]+reduce(lambda a,b:a+b,[[float(iN)/totalSamples/ts[1]]*2 for iN in N])+[0],label="Data")
	p.plot(ct,H,label="sampled")
	p.figure()
        N=[sum(H[j] for j in range(len(H)) if ts[i]<ct[j]<ts[i+1]) for i in range(n)]

	p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),[0]+reduce(lambda a,b:a+b,[[float(iN)/totalSamples/ts[1]]*2 for iN in N])+[0],label="Data")
	N=[sum(HN[j] for j in range(len(H)) if ts[i]<ct[j]<ts[i+1]) for i in range(n)]

	p.plot(reduce(lambda a,b:a+b,[[t]*2 for t in ts]),[0]+reduce(lambda a,b:a+b,[[float(iN)/totalSamples/ts[1]]*2 for iN in N])+[0],label="Data")
	p.show()
	#p.figure()
	#p.plot(noise,'.')
	#p.plot(c**2,'.')
	#print "noise"
	#print np.std(noise)
	#print np.mean(noise)
	print c**2/(np.exp(-s1/lifetime)*lifetime-np.exp(-s2/lifetime)*lifetime+c**2*(s2-s1))*(s2-s1)
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
	print "lik"
	print 
	print likelyhood
	print np.std(ensembleLikelyhood)
	print np.mean(ensembleLikelyhood)





	print lifetime
	print sum(ensemblelifetime)/ensembleSize
	print np.std(ensemblelifetime)

	print sum(noise)/ensembleSize
	print np.std(noise)
	p.show()











