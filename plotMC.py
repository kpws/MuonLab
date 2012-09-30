from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import peakShapes as ps
import random

fig=plt.figure()
ax=Axes3D(fig)
#ax.set_aspect(1,'datalim')
MAX = max(ps.height/2,ps.d/2)*1.1
for direction in (-1, 1):
        for point in np.diag(direction * MAX * np.array([1,1,1])):
                    ax.plot([point[0]], [point[1]], [point[2]], 'w')

def inGeo(x, y):
    return 0<x<ps.width and 0<y<ps.height and x>ps.k*(y-ps.turnY) and x<ps.width-ps.k*(y-ps.turnY)

dxm=0.5
for dx in [-dxm,dxm]:
    for z in [-ps.d/2,ps.d/2]:
        ax.plot3D(np.array([-ps.width/2,-ps.width/2,-ps.a/2,ps.a/2,ps.width/2,ps.width/2,-ps.width/2])+dx,
            [-ps.height/2,ps.turnY-ps.height/2,ps.height/2,ps.height/2,ps.turnY-ps.height/2,-ps.height/2,-ps.height/2],[z]*7,'k')

    n=100
    for i in range(n):
        if dx==-dxm:
            x1=random.random()*ps.width
            y1=random.random()*ps.height
        else:
            x1=ps.width/2
            y1=ps.sourceY
        if not inGeo(x1, y1):
            continue
        phi=random.random()*2*np.pi
        cosTheta=random.random()*(1-ps.minCosTheta)+ps.minCosTheta
        x2=x1+np.cos(phi)*ps.d*np.sqrt(1-cosTheta**2)/cosTheta
        y2=y1+np.sin(phi)*ps.d*np.sqrt(1-cosTheta**2)/cosTheta#np.tan(theta)*d
        extra=1.1 if dx==-dxm else 0.0
        if inGeo(x2, y2):
            ax.plot([x1-ps.width/2+dx,x2-ps.width/2+dx],[y1-ps.height/2,y2-ps.height/2],[-ps.d/2,ps.d/2],'.-b' if dx==-dxm else '.-r')
            ax.plot([x2+(x1-x2)*extra-ps.width/2+dx,x1+(x2-x1)*extra-ps.width/2+dx],[y2+(y1-y2)*extra-ps.height/2,y1+(y2-y1)*extra-ps.height/2],[-ps.d/2*(1+2*(extra-1)),ps.d/2*(1+2*(extra-1))],'-b' if dx==-dxm else '-r')
            ax.plot([x1-ps.width/2+dx,dx],[y1-ps.height/2,ps.height/2],[-ps.d/2,-ps.d/2],'--y')
            ax.plot([x2-ps.width/2+dx,dx],[y2-ps.height/2,ps.height/2],[ps.d/2,ps.d/2],'--y')
#ax.axis('equal')
#plt.xlabel('[m]')
#plt.ylabel('[m]')
#ax.set_zlabel('[m]')
#ax.grid(False)
ax.set_axis_off()
ax.set_frame_on(False)
plt.savefig('mc.pdf',bbox_inches=0)
plt.show()
