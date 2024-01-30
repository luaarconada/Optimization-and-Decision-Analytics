# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 16:51:26 2023

@author: Usuario
"""

from gurobipy import *
import numpy as np
import itertools

# Number of cities
n = 8

# List [1,...,8]
oneton = range(1, n+1)

# Set={1,...,8}
N = set(oneton)


# Introduce the data
c = np.empty((n,n))

c[0,1:] = [295, 508, 505, 348, 867, 419, 305]

c[1,2:] = [790, 315, 166, 883, 582, 520]

c[2,3:] = [860,844,894,619,539]

c[3,4:] = [166,976,298,333]

c[4,5:] = [799,361,345]

c[5,6:] = [510,636]

c[6,7:] = [165]

for (i,j) in itertools.product(oneton, oneton):
    c[j-1,i-1] = c[i-1,j-1]
    
for i in oneton:
    c[i-1,i-1] = 0
    
route, c = multidict({(i,j): c[i-1,j-1] for (i,j) in itertools.product(oneton, oneton)})


# Create model and name it
model = Model('ex3')

x = model.addVars(route, obj=c, name="x", vtype=GRB.BINARY)


# Constraints    
model.addConstrs((quicksum(x[i,j] for j in oneton if j != i) == 1 for i in oneton),
                 "At least 1 arrow in")

model.addConstrs((quicksum(x[j, i] for j in oneton if j != i) == 1 for i in oneton),
                 "At least 1 arrow out")


# Iterations
# 1st iteration
S0 = {6,7}
S0_not = N - S0
model.addConstr((quicksum(quicksum(x[i,j] for i in S0) for j in S0_not) >= 1), 
                name='1st iteration')


# 2nd iteration
S1 = {2,4,5}
S1_not = N - S1
model.addConstr((quicksum(quicksum(x[i,j] for i in S1) for j in S1_not) >= 1), 
                name='2nd iteration')


# 3rd iteration
S2 = {1,2}
S2_not = N - S2
model.addConstr((quicksum(quicksum(x[i,j] for i in S2) for j in S2_not) >= 1), 
                name='3rd iteration')


# Objective
obj = quicksum((c[i,j] * x[i,j] for i,j in route))

model.setObjective(obj, GRB.MINIMIZE)

# Disable Presolve
model.setParam(GRB.Param.Presolve, 0)
# Disable Heuristics
model.setParam(GRB.Param.Heuristics, 0)
# Disable Cuts
model.setParam(GRB.Param.Cuts, 0)

model.optimize()


# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')

print('Variable Information:')
                 
for v in model.getVars():
    if v.X != 0:
        print("%s %s %8.2f" % 
              (v.Varname, "=", v.X))
    
        print(" ")
        
print('\nOptimal objective value: %g' % model.objVal)