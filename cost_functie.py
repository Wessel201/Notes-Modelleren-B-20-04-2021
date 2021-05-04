import pandas as pd 
collection_factor = 3
transfer_factor = 1
distribution_factor = 2 

file_name ='Large.xlsx'
class parcel():
	def __init__(self,file):
		xls = pd.ExcelFile(file)
		self.flow = pd.read_excel(xls, 'w')
		self.package_cost = pd.read_excel(xls, 'c')
		self.hub_cost =[13530] + list(pd.read_excel(xls, 'f')[13530])
		self.cities = len(self.flow.columns)

	def calculate_cost(self,hubs):
		cost = 0
		index = {}
		flow_copy = self.flow
		cost_copy = self.package_cost
		cost_copy = cost_copy.take([hub - 1 for hub in hubs])
		cost_copy = cost_copy.drop(columns= 'Unnamed: 0')
		for i in range(1,self.cities):
			if i in hubs:
				index[i] = i
				cost+= self.hub_cost[i-1]
				continue
			nearest_hub = cost_copy.loc[cost_copy[i] > 0 , i].idxmin()
			cost += cost_copy[i][nearest_hub] * flow_copy[i].sum()*collection_factor
			nearest_hub = nearest_hub + 1
			index[i] = nearest_hub
			flow_copy[nearest_hub] = flow_copy[i]+flow_copy[nearest_hub]
			flow_copy = flow_copy.drop(columns = i)
		flow_copy = flow_copy.drop(columns = 'Unnamed: 0')
		for i in range(self.cities - 1):
			# print('index = ' + str(i))
			flowss = list(flow_copy.iloc[i])
			# print(flowss)
			to_hub = index[i+1]
			prices = list(cost_copy[to_hub])
			# print(prices)
			total_packages = sum(flowss)
			transfer_cost = sum([int(flowss[i])*int(prices[i]) for i in range(len(flowss))])
			distribution_cost = self.package_cost[to_hub][i]*total_packages*distribution_factor
			# print(distribution_cost)
			# print(transfer_cost)
			cost+= distribution_cost + transfer_cost
		return cost


		print(flow_copy)




test = parcel(file_name) 
print(test.calculate_cost([1,2,3,9]))

