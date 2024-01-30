# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 17:41:22 2023

@author: Usuario
"""

from gurobipy import *

# Number of different stocks
l = 8

# List [1,...,8]
stocks = range(1,l+1)


# Introduce the data
f_coeff = [-29.50, -26.31, -34.55, -15.23, -62.43, -26.68, -23.85, -31.66]  # Estimated next year

n = [31.80, 24.28, 32.5, 14.16, 50.99, 24.17, 23.67, 28.77]  # Current Price

p = [15.68, 22.1, 30.39, 8.93, 40.55, 18.58, 22.54, 24.84]  # Price Purchased

# I create this list of coefficients because later it is easier with the quicksum in
#the objective function
a_coeff = []
for i in stocks:
    a_coeff.append((0.69 * n[i-1] + 0.3 * p[i-1]))
f = {j: f_coeff[j - 1] for j in stocks}
A = {j: a_coeff[j - 1] for j in stocks}


# Create the model and name it 
model = Model('ex3')


#Decision variables
x = model.addVars(stocks, name="x", lb=0)  # quantity produced


#Constraints
model.addConstr((quicksum(A[i] * x[i] for i in stocks) >= 10000), name="pi")

model.addConstrs(x[i] <= 150 for i in stocks)


# Objective
obj = quicksum((f[j] * x[j]) for j in stocks)

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













