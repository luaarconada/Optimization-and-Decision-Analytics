# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 18:55:47 2023

@author: Usuario
"""

from gurobipy import *

# Number of variables
n = 4

# List [1, ...,n]
oneton = range(1, n + 1)  


# Introduce the data
r_coeff = [55, 32, 84, 75]

A_coeff = [43, 27, 62, 81]

b= 125

r = {j: r_coeff[j - 1] for j in oneton}

A = {j: A_coeff[j - 1] for j in oneton}


# Create model and name it
model = Model('ex1')

# Uncomment next line for linear relaxation (continuous variables)
x = model.addVars(oneton, name="x")

# Uncomment next line for binary variables
# x = model.addVars(oneton, name="x", vtype=GRB.BINARY)

# Uncomment next line for general integer variables
# x = model.addVars(oneton, name="x", vtype=GRB.INTEGER)


# Constraints
model.addConstr((quicksum(A[j] * x[j] for j in oneton)
                           <= b))

model.addConstrs((x[j] <= 1 for j in oneton))


# Valid inequalities
# 1st valid inequality
#model.addConstr(x[1]+x[2]+x[3] <= 2)


# 2nd valid inequality
# model.addConstr(x[3]+x[4]<=1)


# Objective
obj = quicksum(r[j] * x[j] for j in oneton)

model.setObjective(obj, GRB.MAXIMIZE)

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
    print("%s %s %8.2f" % (v.Varname, "=", v.X))
    print(" ")

print('\nOptimal objective value: %g' % model.objVal)






