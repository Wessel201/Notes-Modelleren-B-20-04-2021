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
		self.hub_cost = pd.read_excel(xls, 'f')
		self.cities = len(self.flow.columns)

	def calculate_cost(self,hubs):
		cost = 0
		index = {}
		flow_copy = self.flow
		cost_copy = self.package_cost
		cost_copy = cost_copy.take([hub - 1 for hub in hubs])
		cost_copy = cost_copy.drop(columns= 'Unnamed: 0')
		print(cost_copy)
		for i in range(1,self.cities):
			if i in hubs:
				index[i] = i
				continue
			nearest_hub = cost_copy.loc[cost_copy[i] > 0 , i].idxmin()
			cost += cost_copy[i][nearest_hub] * flow_copy[i].sum()
			nearest_hub = nearest_hub + 1
			print(i,nearest_hub)
			index[i] = nearest_hub
			flow_copy[nearest_hub] = flow_copy[i]+flow_copy[nearest_hub]
			flow_copy = flow_copy.drop(columns = i)
		print(index)
		flow_copy = flow_copy.drop(columns = 'Unnamed: 0')
		print(self.cities)
		for i in range(self.cities - 1):
			print('index = ' + str(i))
			print(flow_copy.iloc[i])
			to_hub = index[i+1]
			print(cost_copy[to_hub])


		print(flow_copy)




test = parcel(file_name) 
test.calculate_cost([1,2,3,9])


