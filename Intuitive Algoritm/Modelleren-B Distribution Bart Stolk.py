import pandas as pd 
collection_factor = 3
transfer_factor = 1
distribution_factor = 2 

file_name ='Small.xlsx'
class parcel():
	def __init__(self,file):
		xls = pd.ExcelFile(file)
		self.flow = pd.read_excel(xls, 'w')
		self.flow = self.flow.transpose()
		self.package_cost = pd.read_excel(xls, 'c')
		self.package_cost = self.package_cost.transpose()
		if file == 'Large.xlsx':
			self.hub_cost =[13530] + list(pd.read_excel(xls, 'f')[13530])
		else:
			self.hub_cost =[4388] + list(pd.read_excel(xls, 'f')[4388])
		self.cities = len(self.flow.columns)

	def calculate_cost(self,hubs):
		cost = 0
		index = {}
		hubs = sorted(hubs)
		flow_copy = self.flow.copy(deep=True)
		flow_copy = flow_copy.drop(index = 'Unnamed: 0')
		cost_copy = self.package_cost.copy(deep=True)
		cost_copy = cost_copy.take([hub for hub in hubs])
		for i in range(self.cities):
			if i+1 in hubs:
				index[i] = i+1
				cost+= self.hub_cost[i]
				continue
			nearest_hub = cost_copy.loc[cost_copy[i] > 0 , i].idxmin()
			cost += cost_copy[i][nearest_hub] * flow_copy[i].sum()*collection_factor
			nearest_hub = nearest_hub 
			index[i] = nearest_hub
			flow_copy[nearest_hub-1] = flow_copy[i]+flow_copy[nearest_hub-1]
			flow_copy = flow_copy.drop(columns = i)
		for i in range(self.cities):
			# print('index = ' + str(i))
			flowss = list(flow_copy.iloc[i])
			to_hub = index[i] - 1 
			prices = list(cost_copy[to_hub])
			total_packages = sum(flowss)
			transfer_cost = sum([int(flowss[i])*int(prices[i]) for i in range(len(flowss))])
			distribution_cost = self.package_cost[to_hub][i+1]*total_packages*distribution_factor
			# print(distribution_cost)13530

			# print(transfer_cost)
			cost+= distribution_cost + transfer_cost
		return cost


		print(flow_copy)


file_name = 'Small.xlsx'
g = parcel(file_name)

def next_lowest(g, hubs): #finds the next best hub to minimalise dist costs
    low = 1e10
    low_id = None
    
    for c in range(1,g.cities):
        #print('low', low, low_id)
        if c in hubs:   #checks if c is already a hub
            continue
        
        else:           #calculates the cost of adding city c as hub
            temp_hubs = sorted(hubs + [c])
            #print(temp_hubs)
            temp_cost = g.calculate_cost(temp_hubs)
            #print('temp', temp_cost, c)
            if temp_cost < low:     #compares to see if it's the lowest
                low = temp_cost
                low_id = c
    return low, low_id


cur_hubs = []
res = []
for _ in range(1, g.cities):
    new_cost, new_hub = next_lowest(g, cur_hubs)
    cur_hubs = sorted(cur_hubs + [new_hub])
    res.append((new_cost, cur_hubs))

print(res)
