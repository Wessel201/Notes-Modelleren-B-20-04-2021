import pandas as pd 


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
		# for i in range(self.cities):
		# 	to_hub = index[i]
		# 	flow_copy.iloc[i]

		print(flow_copy.iloc[14])




test = parcel(file_name) 
test.calculate_cost([1,2,3,9])


print(test.package_cost.loc[test.package_cost[14] > 0, 14].idxmin())
print(test.package_cost[14])
print(test.package_cost)