#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Packages needed
import pybinding as pb
import numpy as np
import cupy as cp
import os
import argparse
import time
import scipy
import sys
from tqdm import tqdm


# In[3]:


#Wilson Loop Calculation
def HamBlk(kx,ky,kz,syst):
    solver= pb.solver.lapack(syst)
    solver.set_wave_vector([kx,ky,kz])
    H=cp.array(getattr((getattr(solver,'model')),'hamiltonian').todense())
    EV, EVec=cp.linalg.eigh(H)
    #=solver.eigenvalues
    #EVec=solver.eigenvectors
    return EV, EVec
def proj(kx,ky,kz,syst,bnds):
    w,v=HamBlk(kx,ky,kz,syst)
    #w,v=np.linalg.eigh(H)
    ft=cp.zeros(cp.shape(cp.outer(cp.transpose(cp.conjugate(v[:,[0]])),v[:,[0]])))
    for i in bnds:
        ft=ft+cp.outer(v[:,[i]],cp.transpose(cp.conjugate(v[:,[i]])))
    return ft
def eig(kx,ky,kz,syst,bnds):
    w,v=HamBlk(kx,ky,kz,syst)
    #w,v=np.linalg.eigh(H)
    return v[:,bnds]

def WSurf(vec,syst,bnds,ds,ds2,rvec0):
    #rvec0 = np.array(lat.reciprocal_vectors())
    rvec=np.zeros((3,3))
    for j in range(np.shape(rvec0)[0]):
        rvec[j]=rvec0[j]
    #rvec=cp.asnumpy(rvec)
    WCC=[]
    #rf3=np.dot(rvec,vec(0,1))
    #kp = np.linspace(0,rf3,ds2)
    for kk1 in range(int(ds2+1)):
        kk=np.dot(vec(0,kk1/ds2),rvec)
        rf=np.dot(vec(1,0),rvec)
        rf2=np.dot(vec(1,0),rvec)+kk
        #rf=cp.array(rf)
        #rf2=cp.array(rf2)
        #kk=cp.array(kk)
        kpts=np.linspace(rf/ds+kk,rf-rf/ds+kk,ds)
        w,v=HamBlk(rf2[0],rf2[1],rf2[2],syst)
        #w,v=np.linalg.eigh(H)
        sp=v[:,bnds]
        ft=proj(rf2[0],rf2[1],rf2[2],syst,bnds)
        ff=ft
        for i in kpts:
            ft=cp.dot(ft,proj(i[0],i[1],i[2],syst,bnds))
        ft=cp.dot(ft,ff)
        WCC.append(np.imag(np.log(np.linalg.eigvals(cp.asnumpy(cp.dot(cp.dot(cp.transpose(cp.conjugate(sp)),ft),sp))))))
    return cp.asnumpy(cp.array(WCC))

import scipy
def projnwl(WCC, bnds2):
    v=cp.array(WCC)
    ft=cp.zeros(cp.shape(cp.outer(cp.transpose(cp.conjugate(v[:,[0]])),v[:,[0]])))
    #ft=np.outer(np.transpose(np.conjugate(v)),v)
    for i in bnds2:
        ft=ft+cp.outer(v[:,[i]],cp.transpose(cp.conjugate(v[:,[i]])))
    return ft
def Hermitize(X):
    return 0.5*(X+cp.conjugate(cp.transpose(X)))
def WNWL(vec,syst,bnds,bnds2,ds,ds2,rvec0):
    #rvec0 = np.array(lat.reciprocal_vectors())
    rvec=np.zeros((3,3))
    for j in range(np.shape(rvec0)[0]):
        rvec[j]=rvec0[j]
    WCC=[]
    #rf3=np.dot(vec(0,1),rvec)
    #kp = np.linspace(0,rf3,ds2)
    for kk1 in range(int(ds2+1)):
        kk=np.dot(vec(0,kk1/ds2),rvec)
        rf=np.dot(vec(1,0),rvec)
        rf2=np.dot(vec(1,0),rvec)+kk
        kpts=np.linspace(rf/ds+kk,rf-rf/ds+kk,ds)
        w,v=HamBlk(rf2[0],rf2[1],rf2[2],syst)
        #w,v=np.linalg.eigh(H)
        sp=v[:,bnds]
        ft=proj(rf2[0],rf2[1],rf2[2],syst,bnds)
        ff=ft
        for i in kpts:
            ft=cp.dot(ft,proj(i[0],i[1],i[2],syst,bnds))
        ft=cp.dot(ft,ff)
        WH=Hermitize(-1j*cp.array(scipy.linalg.logm(cp.asnumpy(cp.dot(cp.dot(cp.transpose(cp.conjugate(sp)),ft),sp)))))
        w, v= cp.linalg.eigh(WH)
        WCC.append(cp.dot(eig(rf2[0],rf2[1],rf2[2],model,bnds),v))
    sp=WCC[0][:,bnds2]
    ft=projnwl(WCC[0],bnds2)
    ff=ft
    for i in range(int(ds2+1)):
        ft=cp.dot(ft,projnwl(WCC[i],bnds2))
    ft=cp.dot(ft,ff)
    return np.imag(np.log(np.linalg.eigvals(cp.asnumpy(cp.dot(cp.dot(cp.transpose(cp.conjugate(sp)),ft),sp)))))

#Spin resolved Wilson loop:
def proj2(kx,ky,kz,syst,bnds,op):
    H=cp.dot(cp.dot(proj(kx,ky,kz,syst,bnds),op),proj(kx,ky,kz,syst,bnds))
    w,v=cp.linalg.eigh(H)
    ft=cp.zeros(cp.shape(cp.outer(cp.transpose(cp.conjugate(v[:,[0]])),v[:,[0]])))
    for i in bnds[:int(cp.shape(bnds)[0]/2)]:
        ft=ft+cp.outer(v[:,[i]],cp.transpose(cp.conjugate(v[:,[i]])))
    return ft
def WSpinSurf(vec,syst,bnds,ds,ds2,op,rvec0):
    #rvec0 = np.array(lat.reciprocal_vectors())
    rvec=np.zeros((3,3))
    for j in range(np.shape(rvec0)[0]):
        rvec[j]=rvec0[j]
    WCC=[]
    rf3=np.dot(rvec,vec(0,1))
    kp = np.linspace(0,rf3,ds2)
    for kk in kp:
        rf=np.dot(rvec,vec(1,0))
        rf2=np.dot(rvec,vec(1,0))+kk
        kpts=np.linspace(rf/ds+kk,rf-rf/ds+kk,ds)
        H=cp.dot(cp.dot(proj(rf2[0],rf2[1],rf2[2],syst,bnds[:int(cp.shape(bnds)[0]/2)]),op),proj(rf2[0],rf2[1],rf2[2],syst,bnds[:int(cp.shape(bnds)[0]/2)]))
        w,v=cp.linalg.eigh(H)
        sp=v[:,bnds[:int(cp.shape(bnds)[0]/2)]]
        ft=proj2(rf2[0],rf2[1],rf2[2],syst,bnds,op)
        ff=ft
        for i in kpts:
            ft=cp.dot(ft,proj2(i[0],i[1],i[2],syst,bnds,op))
        ft=cp.dot(ft,ff)
        WCC.append(np.imag(np.log(np.linalg.eigvals(cp.asnumpy(cp.dot(cp.dot(cp.transpose(cp.conjugate(sp)),ft),sp))))))
    return cp.asnumpy(cp.array(WCC))
def WSpinLine(kpts,syst,bnds,op):
    WCC=[]
    rf2=kpts[0]
    H=cp.dot(cp.dot(proj(rf2[0],rf2[1],rf2[2],syst,bnds[:int(cp.shape(bnds)[0]/2)]),op),proj(rf2[0],rf2[1],rf2[2],syst,bnds[:int(cp.shape(bnds)[0]/2)]))
    w,v=cp.linalg.eigh(H)
    sp=v[:,bnds[:int(cp.shape(bnds)[0]/2)]]
    ft=proj2(rf2[0],rf2[1],rf2[2],syst,bnds,op)
    ff=ft
    for i in kpts[1:]:
        ft=cp.dot(ft,proj2(i[0],i[1],i[2],syst,bnds,op))
    ft=cp.dot(ft,ff)
    WCC.append(np.imag(np.log(np.linalg.eigvals(cp.asnumpy(cp.dot(cp.dot(cp.transpose(cp.conjugate(sp)),ft),sp))))))
    return cp.asnumpy(cp.array(WCC))

def WLine(kpts,syst,bnds):
    WCC=[]
    #rvec0 = np.array(lat.reciprocal_vectors())
    rf2=kpts[0]
    w,v=HamBlk(rf2[0],rf2[1],rf2[2],syst)
    #w,v=np.linalg.eigh(H)
    sp=v[:,bnds]
    ft=proj(rf2[0],rf2[1],rf2[2],syst,bnds)
    ff=ft
    for i in kpts[1:]:
        ft=cp.dot(ft,proj(i[0],i[1],i[2],syst,bnds))
    ft=cp.dot(ft,ff)
    WCC.append(np.imag(np.log(np.linalg.eigvals(cp.asnumpy(cp.dot(cp.dot(cp.transpose(cp.conjugate(sp)),ft),sp))))))
    return cp.asnumpy(cp.array(WCC))
