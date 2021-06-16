import pandas as pd
import pulp as p
import numpy as np
#Input
cities = range(15)
file = 'Large.xlsx'
xls = pd.ExcelFile(file)

flow = pd.read_excel(xls, 'w')
flow = flow.values[:,1:]
#Flow input

cost = pd.read_excel(xls, 'c')
cost = cost.values[:,1:]
#Cost input

hub_cost = pd.read_excel(xls, 'f')
hub_cost = hub_cost.values[:,1]
hub_cost = np.append([13530], hub_cost)
#Hub costs input

o = dict()
d = dict()
for i in cities:
    o[i] = sum(flow[i,:])
    d[i] = sum(flow[:,i])
#Total flow from nodes and flow to nodes.


#Creating the model
Parcel = p.LpProblem('Parcel', p.LpMinimize)

#Variables
e = p.LpVariable.dicts('Edge', ((i,k) for i in cities
                                      for k in cities), cat='Binary')
#1 if node i is assigned to hub k, 0 otherwise

y = p.LpVariable.dicts('Path', ((i,j,k,l) for i in cities
                                          for j in cities
                                          for k in cities
                                          for l in cities), cat='Binary')
#1 if there is a path i->k->l->j, 0 otherwise

mc = p.LpVariable.dicts('MultC', ((i,j) for i in cities
                                        for j in cities), 0, None, cat='Integer')
#Multiplier for collection
md = p.LpVariable.dicts('MultD', ((i,j) for i in cities
                                        for j in cities), 0, None, cat='Integer')
#Multiplier for distribution
mt = p.LpVariable.dicts('MultT', ((i,j) for i in cities
                                        for j in cities), 0, None, cat='Integer')
#Multiplier for transfer

a = p.LpVariable.dicts('Helper1', ((i,j,k,l) for i in cities
                                             for j in cities
                                             for k in cities
                                             for l in cities), 0, None, cat='Integer')
#Composition of y[(i,j,k,l)] and mc[(i,j)]
b = p.LpVariable.dicts('Helper2', ((i,j,k,l) for i in cities
                                             for j in cities
                                             for k in cities
                                             for l in cities), 0, None, cat='Integer')
#Composition of y[(i,j,k,l)] and md[(i,j)]
c = p.LpVariable.dicts('Helper3', ((i,j,k,l) for i in cities
                                             for j in cities
                                             for k in cities
                                             for l in cities), 0, None, cat='Integer')
#Composition of y[(i,j,k,l)] and mt[(k,l)]

#Objective function

Parcel += p.lpSum(flow[i][j]*(a[(i,j,k,l)]*cost[i][k]+
                              b[(i,j,k,l)]*cost[k][l]+
                              c[(i,j,k,l)]*cost[l][j])
                for i in cities
                for j in cities
                for k in cities
                for l in cities) + p.lpSum(hub_cost[k]*e[k,k] for k in cities)

#Constraints

for i in cities:
    Parcel += p.lpSum(e[(i,k)] for k in cities) == 1
#Every node is assigned to exactly one hub

    for k in cities:
        Parcel += e[(i,k)] <= e[(k,k)]
#A node can only be assigned to another node if that other node is a hub.

for i in cities:
    for j in cities:
        for k in cities:
            for l in cities:
                Parcel += y[(i,j,k,l)] <= e[(i,k)]
                Parcel += y[(i,j,k,l)] <= e[(j,l)]
                Parcel += y[(i,j,k,l)] >= e[(i,k)] + e[(j,l)] - 1
#With these: y[(i,j,k,l)] = e[(i,k)]*e[(l,j)]
                Parcel += a[(i,j,k,l)] <= 26*y[(i,j,k,l)]
                Parcel += a[(i,j,k,l)] <= mc[(i,k)]
                Parcel += a[(i,j,k,l)] >= mc[(i,k)] - 26*(1-y[(i,j,k,l)])
                Parcel += a[(i,j,k,l)] >= 0
#With these: a[(i,j,k,l)] = y[(i,j,k,l)]*mc[(i,k)]                
                Parcel += b[(i,j,k,l)] <= 26*y[(i,j,k,l)]
                Parcel += b[(i,j,k,l)] <= mt[(k,l)]
                Parcel += b[(i,j,k,l)] >= mt[(k,l)] - 26*(1-y[(i,j,k,l)])
                Parcel += b[(i,j,k,l)] >= 0
#With these: b[(i,j,k,l)] = y[(i,j,k,l)]*mt[(k,l)]                 
                Parcel += c[(i,j,k,l)] <= 26*y[(i,j,k,l)]
                Parcel += c[(i,j,k,l)] <= md[(l,j)]
                Parcel += c[(i,j,k,l)] >= md[(l,j)] - 26*(1-y[(i,j,k,l)])
                Parcel += c[(i,j,k,l)] >= 0
#With these: c[(i,j,k,l)] = y[(i,j,k,l)]*md[(l,j)] 

for i in cities:
    for j in cities:
        Parcel += mc[(i,j)] >= (e[(i,j)]*o[i])/100
        Parcel += mc[(i,j)] <= (e[(i,j)]*o[i] + 99)/100
#mc[(i,j)] is the integer value just above the flow between i and j divided by 100
        Parcel += md[(i,j)] >= (e[(j,i)]*d[j])/100
        Parcel += md[(i,j)] <= (e[(j,i)]*d[j] + 99)/100
#md[(i,j)] is the integer value just above the flow between i and j divided by 100
for k in cities:
    for l in cities:        
        Parcel += mt[(k,l)] >= (p.lpSum(y[(i,j,k,l)]*flow[(i,j)] for i in cities
                                                                 for j in cities))/100
        Parcel += mt[(k,l)] <= (p.lpSum(y[(i,j,k,l)]*flow[(i,j)] for i in cities
                                                                 for j in cities) + 99)/100
#mt[(k,l)] is the integer value just above the flow between k and l divided by 100    
    
Parcel += p.lpSum(e[(k,k)] for k in cities) >= 1
#There must be at least one hub

solver = p.CPLEX_CMD()
res = Parcel.solve(solver)
print("status:", res)
print("OPT:", p.value(Parcel.objective))
