# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 16:51:05 2023

@author: Usuario
"""

from gurobipy import *

# Number of intervals
m=7  

# Number of products
n = 3

# Number of resource constraints
l= 4

# List [1,...,7]
zerotone = range(1,m+1)

# List [1,...,3]
oneton = range(1, n+1)

#List [1...,4]
twotone = range(1,l+1)


# Introduce the data
A = [[12, 15, 10],
     [15, 14, 12],
     [11, 13, 9 ],
     [13, 12, 15]]

b = [1500, 1900, 1800, 1200]

fixed_coeff = [40, 50, 45]

profit_coeff = [4, 3, 6, 4, 5, 2.50, 1] 

intervals_coeff = [10, 50, 8, 50, 10, 10, 40]

profit = {j: profit_coeff[j-1] for j in zerotone}

fixed = {j: fixed_coeff[j-1] for j in oneton}

intervals = {j: intervals_coeff[j-1] for j in zerotone}


# Create model and name it
m = Model('ex2')

x = m.addVars(oneton, name='x', lb=0,  ub=60, vtype=GRB.INTEGER)

y = m.addVars(zerotone, name='y', vtype=GRB.BINARY)

z = m.addVars(zerotone, name='z', lb=0, vtype=GRB.INTEGER)

t = m.addVars(oneton, name='t', vtype=GRB.BINARY)



# Constraints
# Constraints for Product 1
index1 = [1,2]

m.addConstr((quicksum(y[i] for i in index1) == 1), name='y1 + y2 = 1')

m.addConstr((quicksum(z[i] for i in index1) == x[1]), name='z1 + z2 = x1')

m.addConstr((z[1] <= 10*y[1]), name='z1 <= 10y1')

m.addConstr((10*y[2] <= z[2]), name='10y <= z2')

m.addConstr((z[2] <= 60*y[2]), name='z2 <= 60y2')



# Constraints for Product 2
index2 = [3,4]

m.addConstr((quicksum(y[i] for i in index2) == 1), name='y3 + y4 = 1')

m.addConstr((quicksum(z[i] for i in index2) == x[2]), name='z3 + z4 = x2')

m.addConstr((z[3] <= 8*y[3]), name='z3 <= 8y3')

m.addConstr((8*y[4] <= z[4]), name='8y4 <= z4')

m.addConstr((z[4] <= 60*y[4]), name='z4 <= 60y4')


# Constraints for Product 3
index3 = [5,6,7]

m.addConstr((quicksum(y[i] for i in index3) == 1), name='y5 + y6 + y7 = 1')

m.addConstr((quicksum(z[i] for i in index3) == x[3]), name='z5 + z6 + z7 = x3')

m.addConstr((z[5] <= 10*y[5]), name='z5 <= 10y5')

m.addConstr((10*y[6] <= z[6]), name='10y6 <= z6')

m.addConstr((z[6] <= 20*y[6]), name='z6 <= 20y6')

m.addConstr((20*y[7] <= z[7]), name='20y7 <= z7')

m.addConstr((z[7] <= 60*y[7]), name='z7 <= 60y7')


# Additional constraints
# Fixed prices
m.addConstrs(((x[i] <= 60*t[i]) for i in oneton), name='Fixed prices')


# Resource availability
m.addConstrs((quicksum(A[i-1][j-1] * x[j] for j in oneton) <= b[i-1]
              for i in twotone), name='Resource availability')


# If x_3 > 0, then x_1 > 0
m.addConstr((x[3] <= 60*t[1]), name='x3>0 => x1>0')



# Objective
index5 = zerotone
obj = -quicksum(fixed[i] * t[i] for i in oneton) +\
      quicksum(profit[i] * z[i] for i in index5) +\
      profit[1]*intervals[1]*y[2] - profit[2]*intervals[1]*y[2] +\
      profit[3]*intervals[3]*y[4] - profit[4]*intervals[3]*y[4] +\
      profit[5]*intervals[5]*y[6] - profit[6]*intervals[5]*y[6] +\
      (profit[5]*intervals[5] + profit[6]*intervals[6])*y[7] -\
      profit[7]*(intervals[5] + intervals[6]) * y[7]
      
m.setObjective(obj, GRB.MAXIMIZE)

# Disable Presolve
m.setParam(GRB.Param.Presolve, 0)
# Disable Heuristics
m.setParam(GRB.Param.Heuristics, 0)
# Disable Cuts
m.setParam(GRB.Param.Cuts, 0)

m.optimize()


# Display solution (print the name of each variable and the solution value)
print('--------------------------------')
print('\nOptimal solution:\n')

print('Variable Information:')
                 
for v in m.getVars():
    print("%s %s %8.2f" % 
              (v.Varname, "=", v.X))
    
    print(" ")
        
print('\nOptimal objective value: %g' % m.objVal)




