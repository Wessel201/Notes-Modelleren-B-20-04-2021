from pulp import *
import pandas as pd
import cplex 
col = 3
trns = 1
dist = 2 
N = range(15)
file_name ='Large.xlsx'
xls = pd.ExcelFile(file_name)
flow = pd.read_excel(xls, 'w')
p_cost = pd.read_excel(xls, 'c')
hub_cost =[13530] + list(pd.read_excel(xls, 'f')[13530])
flow = flow.values[:,1:]
p_cost = p_cost.values[:,1:]

model = LpProblem('ParcelTransport', sense=LpMinimize)

isHub = LpVariable.dicts('isHub', N, 0, 1, LpBinary)


hasEdge = LpVariable.dicts("hasEdge", [(i,j) for i in N
                                       for j in N],
                           0, 1, LpBinary)
y = LpVariable.dicts("y", [(i,j) for i in N
                                       for j in N],
                           0, 1, LpBinary)

x = LpVariable.dicts("x", [(i,j) for i in N
                                       for j in N],
                           0, 1, LpBinary)

model += lpSum(flow[i][j]*(col*p_cost[i][k]*hasEdge[i,k]+
                           (trns*p_cost[k][l]+dist*p_cost[l][j])*hasEdge[l,j])
               for i in N
               for j in N
               for k in N
               for l in N)
+ lpSum(hub_cost[i]*isHub[i] for i in N)

for i in N:
    model += hasEdge[(i,i)] - isHub[i] == 0
    model += lpSum(y[(i,j)] for j in N) == 1
    model += lpSum(x[(i,j)] for j in N) == 1
    for j in N:
        model += y[(i,j)] <= 1-isHub[i]
        model += y[(i,j)] <= hasEdge[(i,j)]
        model += y[(i,j)] >= hasEdge[(i,j)] - isHub[i]
        model += x[(i,j)] <= y[(i,j)]
        model += x[(i,j)] <= isHub[j]
        model += x[(i,j)] >= y[(i,j)] + isHub[j] - 1
model += lpSum(isHub[i] for i in N) >= 1

sol = model.solve(CPLEX_CMD())
print(LpStatus[sol])