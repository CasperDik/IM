# -*- coding: utf-8 -*-

"""
Created on Thu May  5 19:35:23 2022

@author: josel
"""
from gurobipy import Model, GRB, quicksum


setup = [100,150,180]
h = 1
demand = [10,10,70,10,20,80]
D = {i: demand[i-1] for i in range(1, len(demand) + 1)}
T = len(D)
S = 3


av = [[0,0,1,0,0,1], [0,1,0,0,1,0], [1,1,1,1,1,1]]
cap = [80,70,50]
A = {(n,s): av[s-1][n-1] for s in range (1,S + 1) for n in range (1,T + 1)}
W = {i:cap[i-1] for i in range (1, S + 1)}
K = {i:setup[i-1] for i in range(1,S+1)}

model = Model()
M = sum(demand)
#M = 80
y = {}
Q = {}
I = {0:0}

# Define variables
for n in range (1,T + 1):
    I[n] = model.addVar(vtype = 'C', lb = 0)
    
    for s in range (1, S + 1):
        y[n,s] = model.addVar(vtype = 'B')
        Q[n,s] = model.addVar(vtype = 'C', lb = 0)
    
# Define objective function

model.setObjective (quicksum( h * I[n] for n in range (1,T + 1)) + 
                    quicksum(K[s] * y[n,s] for n in range (1,T + 1) for s in range(1,S + 1)), GRB.MINIMIZE)

# Define constraints

for n in range (1,T + 1):
    model.addConstr (I[n] == I[n-1] + quicksum(Q[n,s] for s in range (1,S + 1)) - D[n])
    for s in range (1,S + 1):
        model.addConstr (Q[n,s] <= A[n,s] * W[s] * y[n,s])
    
# optimize

model.optimize()

# Print solution

print([((n,s), (Q[n,s].x)) for n in range (1,T+1) for s in range(1,S + 1) if y[n,s].x > 0])
print('The optimal cost is:', round(model.objval,1))