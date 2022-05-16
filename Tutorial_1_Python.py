#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy as np
import matplotlib.pyplot as plt

D = 20         # demand per month
c0 = 1         # unit cost bracket 1
c1 = 0.9       # unit cost bracket 2
c2 = 0.85      # unit cost bracket 3
alpha = 0.1    # interest rate holding costs per unit per month
K = 100        # ordering cost
Q1 = 100       # first bracket limit (up to Q1 no disccount)
Q2 = 200       # second bracket limit 


# In[15]:


def EOQ (D,c,alpha,K):
    return np.sqrt(2 * K * D / (alpha * c))

def EOQ_incremental (v,D,c,alpha,K):
    return np.sqrt(2 * (K + v) * D / (alpha * c))

def Qapplicable (Q,mn,mx):
    if Q <mn:
        return mn
    elif Q > mx:
        return mx
    return Q
    
def C(Q,D,c,alpha,K):
    return Q * c * alpha / 2 + K * D / Q + D * c

def C_incremental(v,Q,D,c,alpha,K):
    return alpha * v / 2 + alpha * c * Q/2 + (K + v) * D/ Q + c * D


# In[18]:


##### ALL UNIT DISCCOUNT CASE #######

# STEP 1: COMPUTE EOQ

Qstar1 = EOQ (D,c0,alpha,K)
Qstar2 = EOQ (D,c1,alpha,K)
Qstar3 = EOQ (D,c2,alpha,K)

#STEP 2: IS QSTAR WITHIN THE ALLOWED RANGE?

Qapp1 = Qapplicable (Qstar1,0,Q1)
Qapp2 = Qapplicable (Qstar2,Q1 + 1,Q2)
Qapp3 = Qapplicable (Qstar3,Q2 + 1,999999)

#STEP 3: COMPUTE THE COST OF Q APPLICABLE

Capp1 = C(Qapp1,D,c0,alpha,K)
Capp2 = C(Qapp2,D,c1,alpha,K)
Capp3 = C(Qapp3,D,c2,alpha,K)

print(Capp1,Capp2,Capp3)


# In[24]:


##### INCREMENTAL DISCCOUNT #######
# STEP 1: COMPUTE EOQ

v0 =0
v1 = v0 + (c0 - c1) * Q1
v2 = v1 + (c1 - c2) * Q2

Qstar1 = EOQ_incremental (v0,D,c0,alpha,K)
Qstar2 = EOQ_incremental (v1,D,c1,alpha,K)
Qstar3 = EOQ_incremental (v2,D,c2,alpha,K)

#STEP 2: IS QSTAR WITHIN THE ALLOWED RANGE?

Qapp1 = Qapplicable (Qstar1,0,Q1)
Qapp2 = Qapplicable (Qstar2,Q1 + 1,Q2)
Qapp3 = Qapplicable (Qstar3,Q2 + 1,999999)

#STEP 3: COMPUTE THE COST OF Q APPLICABLE

Capp1 = C_incremental(v0,Qapp1,D,c0,alpha,K)
Capp2 = C_incremental(v1,Qapp2,D,c1,alpha,K)
Capp3 = C_incremental(v2,Qapp3,D,c2,alpha,K)

print(Capp1, Capp2,Capp3)


# In[26]:


# PLOT INCREMENTAL
Qs = range (50, 350)
Cs1 = [C_incremental(v0,quantity,D,c0,alpha,K) for quantity in Qs]
Cs2 = [C_incremental(v1,quantity,D,c1,alpha,K) for quantity in Qs]
Cs3 = [C_incremental(v2,quantity,D,c2,alpha,K) for quantity in Qs]
plt.plot (Qs,Cs1)
plt.plot (Qs,Cs2)
plt.plot (Qs,Cs3)
plt.axvline(x=Q1,ls='--')
plt.axvline(x=Q2,ls='--')

