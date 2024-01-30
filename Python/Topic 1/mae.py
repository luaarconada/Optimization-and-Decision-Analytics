from gurobipy import *

n = 6 # number of observations

oneton = range(1, n+1)  # list [1, ..., n]

zerotoone = range(2) # list [0, 1]

x_data = [29.7, 29.7, 31.4, 31.8, 27.6] 

y_data = [175.3, 177.8, 185.4, 175.3, 172.7]

x = {j : x_data[j-1] for j in oneton}

y = {j : y_data[j-1] for j in oneton}

model = Model('mae')

ePlus = model.addVars(oneton, name="ePlus")

eMinus = model.addVars(oneton, name="eMinus")

b = model.addVars(zerotoone, name="b", lb=-GRB.INFINITY)

model.addConstrs((ePlus[i] - eMinus[i] + b[0] + x[i] * b[1] == y[i]
                            for i in oneton), name = "pi")

# Objective
obj = quicksum(((ePlus[i] + eMinus[i]) for i in oneton))

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



