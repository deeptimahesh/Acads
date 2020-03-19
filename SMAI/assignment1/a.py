#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:

data , labels = [], []
data = pd.read_csv('sample_train.csv').to_numpy()
data = data[:,1:]
labels = data[:,0]
data = data - np.mean(data,axis=0)


# In[3]:




C = np.cov(data.T)
(_, D) = np.linalg.eigh(C)
D = D.T[::-1].T



def display(data, labels, title):
    i = 0
    while i < 10:
        i+=1
        d = data[labels==i]
        plt.figure()
        plt.xlabel('X')
        plt.subplots_adjust(top=3, right=3)
        plt.title(title, fontsize=25)
        plt.ylabel('X')
        plt.scatter(d[:,0],d[:,1],s=2)
# In[5]:


proj = np.matmul(data, D[:, :2])
display(proj, labels, "PCA No GD")


# In[6]:

def calc_del_noreg(X, C): 
    F = np.matmul(X, np.matmul( C , C.T))
    P = F - X
    T1 = np.matmul(X.T, np.matmul( P ,C))
    T2 = np.matmul(P.T, np.matmul(X ,C))
    scale = np.linalg.norm(F)
    J = (T1 + T2)/ scale
    return J


# In[7]:





# In[8]:


def calc_del_l1(X, C): 
    F = np.matmul(X, np.matmul(C,C.T))
    P = F - X
    T1 = np.matmul(X.T,np.matmul( P, C))
    T2 = np.matmul(P.T, np.matmul( X,C))
    scale = np.linalg.norm(F)
    J = (T1 + T2)/ scale + 0.005 * (np.matmul(X.T, np.sign(np.matmul(X,C))) + np.sign(C))
    return J


# In[9]:


def calc_del_l2(X, C): 
    F = np.matmul(X ,np.matmul(C,C.T))
    P = F - X
    T1 = np.matmul(X.T, np.matmul(P,C))
    T2 = np.matmul(P.T, np.matmul(X,C))
    scale = np.linalg.norm(F)
    scale2 = np.linalg.norm(np.matmul(X ,C))
    scale3 = np.linalg.norm(C)
    J = (T1 + T2)/ scale + 0.005 * ((np.matmul(X.T, np.matmul( X ,C)))/scale2 + C/scale3)
    return J


# In[14]:


def grd_noreg(data,alpha,iters):
    w = np.random.rand(784, 784)
    C,_ = np.linalg.qr(w)
    for i in range(iters):
        dell = calc_del_noreg(data, C)
        C = C - alpha * dell
    return C 


# In[21]:


def grd_l1(data,alpha,iters):
    w = np.random.rand(784, 784)
    C,_ = np.linalg.qr(w)
    for i in range(iters):
        dell = calc_del_l1(data, C)
        C = C - alpha * dell
    return C    


# In[16]:



def grd_l2(data,alpha,iters):
    w = np.random.rand(784, 784)
    C,_ = np.linalg.qr(w)
    for i in range(iters):
        dell = calc_del_l2(data, C)
        C = C - alpha * dell
    return C   


# In[17]:


alpha = 0.000007
iters = 120
basis_noreg = grd_noreg(data, alpha, iters)


# In[19]:


projected_noreg = np.matmul(data, basis_noreg[:, :2])
display(projected_noreg,labels, "PCA GD")


# In[22]:

iters = 120
bs = 0.1
alpha = 0.000007
basis_l1 = grd_l1(data, alpha, iters)


# In[23]:


projected_l1 = np.matmul(data, basis_l1[:, :2])
display(projected_l1,labels, "PCA GD L1")


# In[ ]:


alpha = 0.000007
iters = 120
basis_l2 = grd_l2(data, alpha, iters)


# In[ ]:


projected_l2 = np.matmul(data,basis_l2[:, :2])
display(projected_l2,labels, "PCA GD - L2")  


# In[ ]: