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
h = p.LpVariable.dicts('isHub', cities, cat='Binary')

e = p.LpVariable.dicts('hasEdge', ((i,j) for i in cities
                                         for j in cities), cat='Binary')

x = p.LpVariable.dicts('Helper1', ((i,j) for i in cities
                                         for j in cities), cat='Binary')

y = p.LpVariable.dicts('Helper2', ((i,j,k,l) for i in cities
                                          for j in cities
                                          for k in cities
                                          for l in cities), cat='Binary')

a = p.LpVariable.dicts('Helper4', ((i,j) for i in cities
                                         for j in cities), cat='Binary')
#Objective function

Parcel += p.lpSum(flow[i][j]*(col*cost[i][k]+
                           trns*cost[k][l]+dist*cost[l][j])
               for i in cities
               for j in cities
               for k in cities
               for l in cities) + p.lpSum(hub_cost[i]*h[i] for i in cities)
#col*cost[i][k]*e[(i,k)] and (trns*cost[k][l]+dist*cost[l][j])*e[(l,j)] are not
#dependent on eachother. So the first part gets added whenever e[(i,k)]=1 and
#the second part whenever e[(l,j)] = 1. While it is only supposed to happen
#when both of them are 1.

#Constraints
for i in cities:
    Parcel += e[(i,i)] - h[i] == 0
    #Hubs are connected to themselves, cities are not
    
    Parcel += p.lpSum(e[(i,j)] for j in cities) >= 1
    #Every city is collected to at least one other city.
    
    Parcel += p.lpSum(x[(i,j)] for j in cities) <= 1
    #Every city is connected to exactly one hub.
    
    for j in cities:
        Parcel += x[(i,j)] <= e[(i,j)]
        Parcel += x[(i,j)] <= (1-h[i])
        Parcel += x[(i,j)] >= e[(i,j)] + (1-h[i]) - 1
        #Helper function, see lecture notes 2.5
        
        Parcel += a[(i,j)] <= h[i]
        Parcel += a[(i,j)] <= h[j]
        Parcel += a[(i,j)] >= h[i] + h[j] - 1
        
        Parcel += e[(i,j)] >= a[(i,j)]
        #There must be connections between hubs.
  
        Parcel += e[(i,j)] == e[(j,i)]
        #Makes the graph undirected.
        
        Parcel += e[(i,j)] <= h[i] + h[j]
        #No connections between cities

    Parcel += p.lpSum(h[i] for i in cities) >= 1
    #There needs to be at least one hub.
    
solver = p.CPLEX_CMD()
res = Parcel.solve(solver)
print("status:", res)
print("OPT:", p.value(Parcel.objective))
