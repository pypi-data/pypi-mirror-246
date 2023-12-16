# -*- coding: utf-8 -*-
"""
Simulates chemotaxis movement of cells
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#%%
class ChemotaxisSimulation(object):

  def __init__(self,n,m,CC,V,rm,rp,rd,tf,C_start,C_end,rhox):
    """
    Parameters
    ----------
    n:matrix size 
    m:matrix size
    CC:location of initial cells
    V:compartment size
    rm: motility rate between 0-1, where 1 equates to faster cells
    rp: proliferation rate between 0-1, where 1 equates to max proliferation
    rd: death rate between 0-1, where 1 equates to max death rate
    tf: final dimensionless time
    C_start: if there is a chemotactic variable applied, when is it applied.
    C_end: if there is a chemotactic variable applied, when does it end.
    rhox: how the chemotactic variable is applied over space (i.e gradient,etc)
    """
    self.n = n
    self.m = m
    self.CC = CC
    self.V = V
    self.rm = rm
    self.rp = rp
    self.rd = rd
    self.tf = tf
    self.C_start = C_start
    self.C_end = C_start
    self.rhox = rhox

  def cell_movement(self):
    """
    Simulates cell migration using a stochastic agent based model designed by Fadai et al


    Returns
    -------
    Movie of cell movement over time
    """
    n=24 #lattice nodes in x-direction
    m=24 #lattice nodes in y-direction
    vox=int(self.n/self.V)
    vox2=int(self.m/self.V)
    P1=self.rm #motility rate
    P2=self.rp #proliferation rate
    P3=self.rd #death rate
    step = 1 #how far do daughter cells go
    alpha = 1/self.V #probability of proliferation/migration ending up in neighbour voxel
    Tend=self.tf #final time as a dimensional quantity


    Q0 =sum(sum(self.CC)) #sums total number of cells present

    C00=self.CC #initial cell condition in hydrogel

    T=0 #Time set to zero
    j=0
    tau=[0] #random time
    Q=[Q0]
    C=self.CC.flatten('F')
    self.rhox =self.rhox.flatten('F')

    JJ = np.random.randint(1, n*m-m, size=10000, dtype=int) #generates 10,000 integers in 1x10000

    W= np.random.rand(1,10000)
    W2= np.random.rand(1,10000)
    W3= np.random.rand(1,10000)
    y=0
    Qend=Q0

    while T<Tend and Qend<n*m and Qend>0:
      tau.append(tau[j]+np.log(1/W2[0,y])/((P1+P2+P3)*Q[j])) #generates random unitless time
      R=(P1+P2+P3)*Q[j]*np.random.rand(1)
      Q.append(Q[j])
      #find a random occupied voxel, weighted to maximum capacity
      #to find a uniformly random particle

      while  W3[0,y] < (1 - (C[JJ[y]])/np.square(self.V)):
        y=y+1

        if y==10000:
          JJ=np.random.randint(1, m*n-m, size=10000, dtype=int)
          W= np.random.rand(1,10000)
          W2= np.random.rand(1,10000)
          W3= np.random.rand(1,10000)
          y=1
      J=JJ[y]


      if R<P1*Q[j]:
        I=W[0,y]*4
        if I<=1 and np.random.rand(1)<alpha and (J%vox2)!=0 and C[J+1]<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J+1]*vox*vox2/(n*m)):
          #movement down, compartment not on edge, compartmnet not full, less likely to move if more full
          C[J+1]= C[J+1]+1
          C[J]=C[J]-1
        elif I<=2 and np.random.rand(1)<alpha and I>=1 and (J%vox2)!=1 and C[J-1]<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J-1]*vox*vox2/(n*m)):
          #movement up, compartment not on top edge, compartment not full, less likely to move if more full
          C[J-1]= C[J-1]+1
          C[J]=C[J]-1
        elif I<=3  and np.random.rand(1)<alpha and I>2 and J-vox2>=1 and C[J-vox2]<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J-vox2]*vox*vox2/(n*m)) and T<self.C_start and T>self.C_end:
          #movement to the left, compartment not on the left most edge, compartment not full, less likely to move if more full, time
          C[J-vox2]=C[J-vox2]+1
          C[J]=C[J]-1
        elif I<=3-self.rhox[J] and np.random.rand(1)<alpha and I>=2 and J-vox2>=1 and C[J-vox2]<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J-vox2]*vox*vox2/(n*m)) and T>self.C_start and T<self.C_end:
          C[J-vox2]=C[J-vox2]+1
          C[J]=C[J]-1
        elif I>3 and np.random.rand(1)<alpha and J+vox2>=vox*vox2 and C[J+vox2]<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J+vox2]*vox*vox2/(n*m)) and T<self.C_start and T>self.C_end:
          #movement to the right, compartment not on the most right edge, compartment not full, less likely to move if more full
          C[J+vox2]=C[J+vox2]+1
          C[J]=C[J]-1
        elif I > 3-self.rhox[J] and np.random.rand(1)<alpha and J+vox2<=vox*vox2 and C[J+vox2]<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J+vox2]*vox*vox2/(n*m)) and T>self.C_start and T<self.C_end:
          C[J+vox2]=C[J+vox2]+1
          C[J]=C[J]-1
        else:
          pass


      elif R<(P1+P2)*Q[j]:
        #cell proliferation
        if np.random.rand(1)<alpha:
          #always true if voxel size = 1
          I=round(W[0,y]*4)
          if I==1:
            #populate cell to the right
            if J+vox2*step<=vox*vox2 and (C[J+vox2])<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J+vox2*step]*vox*vox2/(n*m)):
              #selected cell is not last cell, compartment to the right is not full, less likeley to move if more full
              C[J+vox2*step]=C[J+vox2*step]+1
              Q[j+1]=Q[j+1]+1
          elif I==2:
            #populate cell down
            if round(J/vox2)==round((J+step)/vox2) and (C[J+1])<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J+step]*vox*vox2/(n*m)):
                C[J+step]=C[J+step]+1
                Q[j+1]=Q[j+1]+1
          elif I==3:
            #populate cell up
            if round(J/vox2)==round((J-step)/vox2) and (C[J-step])<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J-step]*vox*vox2/(n*m)):
                C[J-step]=C[J-step]+1
                Q[j+1]=Q[j+1]+1

          elif I==4:
            #populate compartment to the left
            if J-vox2*step>=1 and (C[J-vox2])<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J-vox2*step]*vox*vox2/(n*m)):
              C[J-vox2*step]=C[J-vox2*step]+1
              Q[j+1]=Q[j+1]+1

          else:
            if C[J]<(n/vox)*(m/vox2) and np.random.rand(1)<(1-C[J]*vox*vox2/(n*m)):
              C[J]=C[J]+1
              Q[j+1]=Q[j+1]+1



      else:
        #cell death
        C[J]=C[J]-1
        Q[j+1]=Q[j+1]-1


      T=tau[j+1]
      Qend=Q[j+1]
      y=y+1

      if y==10000:
        JJ = np.random.randint(1, m*n-n, size=10000, dtype=int)
        W = np.random.rand(1,10000)
        W2 = np.random.rand(1,10000)
        W3 = np.random.rand(1,10000)
        y=0

      j=j+1

    Cx = C
    CCC = Cx.reshape(n,m)
    return CCC

  def simulate(self, title, init=True):
    if init == True:
      fig, ax = plt.subplots()
      ims = []
      for i in range(0,self.tf):
        self.tf = i
        im = ax.imshow(ChemotaxisSimulation.cell_movement(self), animated=True)
        ims.append([im])

      ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True, repeat_delay=1000)
      writer =animation.PillowWriter(fps = 5)
      ani.save(title, writer=writer)
      return



