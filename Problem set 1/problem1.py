# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 21:13:42 2023

@author: Usuario
"""

from gurobipy import*

# Number of resources
n=2

# Number of activities
m=4

# List [1,...,n]
resources=range(1,n+1)

# List [1,...,m]
activities=range(1,m+1)


# Introduce the data
r_coeff=[2.0, 3.0, 9.0, 6.0]

A_coeff = [[4.0, 1.0, 8.0,  2.0],
     [2.0,  3.0, 4.0, 6.0]]

b_coeff = [30.0, 60.0]

r = {j : r_coeff[j-1] for j in activities}

A = {i : {j : A_coeff[i-1][j-1] for j in activities} 
    for i in resources}

b = {i : b_coeff[i-1] for i in resources}


# Create model and name it
model = Model('ex1')

x = model.addVars(activities, name="x") 


# Constraints
model.addConstrs((quicksum(A[i][j] * x[j] for j in activities)
                           == b[i] 
                            for i in resources), name = "pi")


# Objective
obj = quicksum(r[j] * x[j] for j in activities)

model.setObjective(obj, GRB.MAXIMIZE)
        
model.optimize()


# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')

print('Variable Information Including Sensitivity Information:')

# tVars = PrettyTable(['Variable Name', ' Value', 'ReducedCost', 
#                     ' SensLow', ' SensUp'])  #column headers

for v in model.getVars():
    print("%s %s %8.2f %s %8.2f %s %8.2f %s %8.2f" % 
              (v.Varname, "=", v.X, ", reduced cost = ", abs(v.RC), ", from coeff = ", v.SAObjLow, "to coeff = ", v.SAObjUp))
    print(" ")
        
        
print('\nOptimal objective value: %g' % model.objVal)

print('\nOptimal shadow prices:\n')
for c in model.getConstrs():
    print("%s %s %8.2f %s %8.2f %s %8.2f" % (c.ConstrName, ": shadow price = ", c.Pi, ", from RHS = ", c.SARHSLow, "to RHS = ", c.SARHSUp))
    print(" ")