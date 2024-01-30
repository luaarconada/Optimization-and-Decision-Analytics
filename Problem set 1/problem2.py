# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 20:59:00 2023

@author: Usuario
"""


from gurobipy import*

# Number of observations
n = 6

# List [1, ..., n]
observations = range(1, n+1) 

# List [0, 2]
zerotoone = range(3) 


# Introduce the data
x1_data=[16.9, 17.1, 19.3, 16.8, 15.3, 25.2]

x2_data=[29.7, 30.9, 33.8, 31.8, 27.6, 35.9]

x3_data=[175.3, 177.8, 185.4, 175.3, 172.7, 198.5]

x1 = {j : x1_data[j-1] for j in observations}

x2 = {j : x2_data[j-1] for j in observations}

x3 = {j : x3_data[j-1] for j in observations}


# Create the model and name it
model = Model('ex2')


# Decision variables
ePlus = model.addVars(observations, name="ePlus", lb=0)

eMinus = model.addVars(observations, name="eMinus", lb=0)

b = model.addVars(zerotoone, name="b", lb=-GRB.INFINITY)


# Constraints
model.addConstrs((ePlus[i] - eMinus[i] + b[0] + x1[i] * b[1] + x2[i]*b[2] == x3[i]
                            for i in observations), name = "pi")


# Objective
obj = quicksum(((ePlus[i] + eMinus[i]) for i in observations))

model.setObjective(obj, GRB.MINIMIZE)
        
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





