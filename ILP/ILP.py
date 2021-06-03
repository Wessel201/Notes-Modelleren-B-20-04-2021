import pandas as pd
import pulp as p
import numpy as np
#Input
col = 3
trns = 1
dist = 2
cities = range(15)

file = 'Large.xlsx'
xls = pd.ExcelFile(file)

flow = pd.read_excel(xls, 'w')
flow = flow.values[:,1:]

cost = pd.read_excel(xls, 'c')
cost = cost.values[:,1:]

hub_cost = pd.read_excel(xls, 'f')
hub_cost = hub_cost.values[:,1]
hub_cost = np.append([13530], hub_cost)

#Creating the model
Parcel = p.LpProblem('ParcelDelivery', p.LpMinimize)

#Variables
e = p.LpVariable.dicts('hasEdge', ((i,k) for i in cities
                                         for k in cities), cat='Binary')
#1 if city i is assigned to hub k, 0 otherwise

y = p.LpVariable.dicts('Flow', ((i,j,k,l) for i in cities
                                          for j in cities
                                          for k in cities
                                          for l in cities), cat='Binary')
#1 if i->k->l->j is the path from i to j, 0 otherwise

#Objective function

Parcel += p.lpSum(flow[i][j]*(col*cost[i][k]+
                           trns*cost[k][l]+dist*cost[l][j])*y[(i,j,k,l)]
               for i in cities
               for j in cities
               for k in cities
               for l in cities) + p.lpSum(hub_cost[k]*e[k,k] for k in cities)


#Constraints
for i in cities:
    Parcel += p.lpSum(e[(i,k)] for k in cities) == 1
    #Each city i is connected to exactly one hub k.
    
    for k in cities:
        Parcel += e[(i,k)] <= e[(k,k)]
        #There can only be connections from i to k if k is connected to itself
        #(meaning k is a hub)
        
        for j in cities:
            for l in cities:
                Parcel += y[(i,j,k,l)] <= e[(i,k)]
                Parcel += y[(i,j,k,l)] <= e[(j,l)]
                Parcel += y[(i,j,k,l)] >= e[(i,k)] + e[(j,l)] - 1
#With these constraints: y[(i,j,k,l)] = e[(i,k)]*e[(j,l)]

Parcel += p.lpSum(e[k,k] for k in cities) >= 1
#There must be at least one hub
    
solver = p.CPLEX_CMD()
res = Parcel.solve(solver)
print("status:", res)
print("OPT:", p.value(Parcel.objective))
