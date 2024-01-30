# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 21:53:17 2023

@author: leire
"""

from gurobipy import *


n = 8 # number of cities

cities = range(1, n+1) # list of cities: [1,...,8]

c_coeff = [[0, 295, 508, 505, 348, 867, 419, 305],
     [295, 0, 790, 315, 166, 883, 542, 520],
     [508, 790, 0, 860, 844, 894, 619, 539],
     [505, 315, 860, 0, 166, 976, 298, 333],
     [348, 166, 844, 166, 0, 799, 361, 345],
     [867, 883, 894, 976, 799, 0, 510, 636],
     [419, 542, 619, 298, 361, 510, 0, 165],
     [305, 520, 539, 333, 345, 636, 165, 0]]

C = {i : {j : c_coeff[i-1][j-1] for j in cities} 
    for i in cities}

model = Model('tsp3')

x={}
for i in cities:
    for j in cities:
        if i!=j:
            x[i,j] = model.addVar(vtype = GRB.BINARY, name=f'x_{i}_{j}')
            

# Constraints
model.addConstrs((quicksum(x[i,j] for i in cities if i!=j) == 1 for j in cities), name="fb")
model.addConstrs((quicksum(x[i,j] for j in cities if j!=i) == 1 for i in cities), name="fb")
S1=[2,4,5]
SC1=[1,3,6,7,8]
model.addConstr((quicksum(x[i,j] for i in S1 for j in SC1) >= 1), name="subtour")
S2=[1,2]
SC2=range(3,9)
model.addConstr((quicksum(x[i,j] for i in S2 for j in SC2) >= 1), name="subtour")
S3=[6,7]
SC3=[1,2,3,4,5,8]
model.addConstr((quicksum(x[i,j] for i in S3 for j in SC3) >= 1), name="subtour")

# Objective function
obj = quicksum(x[i,j]*C[i][j] for i in cities for j in cities if i!=j)
model.setObjective(obj, GRB.MINIMIZE)

model.optimize() # solve the model


# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')

print('Variable Information:')
                 
for v in model.getVars():
    print("%s %s %8.2f" % 
              (v.Varname, "=", v.x))
    
    print(" ")
        
print('\nOptimal objective value: %g' % model.objVal)