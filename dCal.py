import pylab as p
import csv
import smooth

with open('dCal') as f:
    H=[]
    for line in f:
        H.append(int(line.split()[1]))
        if len(H)==8190:
            break

#left=175
#right=1995
#Hs=[0]*left+list(smooth.smooth(H[left:right],50))+[0]*(len(H)-right)
#p.plot(H)
#p.plot(Hs,'r')
n=10
Hd=[sum(H[i*n+j] for j in range(n)) for i in range(len(H)/n)]
p.hist(Hd,bins=range(0,len(Hd)*n,n))
p.show()
