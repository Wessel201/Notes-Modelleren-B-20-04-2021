import pandas as pd 
import matplotlib.pyplot as plt
import math
collection_factor = 1
transfer_factor = 1
distribution_factor = 1
bus_capactity = 100

file_name ='data_klein.xlsx'


class parcel():
	def __init__(self,file):
		#Here the data is imported from the excel file and stored and variables to be used later
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
		# hubs are given as input variable in the form of a list so eg. [1,2,5]
		cost = 0
		index = {} 
		hubs = sorted(hubs)
		flow_copy = self.flow.copy(deep=True)
		flow_copy = flow_copy.drop(index = 'Unnamed: 0')
		cost_copy = self.package_cost.copy(deep=True)
		cost_copy = cost_copy.take([hub for hub in hubs])
		# The following loop calculates the cost of collection and building of the hubs. 
		for i in range(self.cities):
			if i+1 in hubs:
				#If statement checks if the hub is in the inputed if yes then the cost to built this hub is added to the total cost
				index[i] = i+1
				cost+= self.hub_cost[i]
				continue
			nearest_hub = cost_copy.loc[cost_copy[i] > 0 , i].idxmin()
			#the nearest hub is determined by finding the hub that has the lowest collection cost for that city 
			cost += cost_copy[i][nearest_hub] * flow_copy[i].sum()*math.ceil(flow_copy[i].sum()/bus_capactity)*collection_factor
			#The amount of packages multiplied by the cost of collection of the nearest hub multiplied by the collection factor is added to the cost 
			nearest_hub = nearest_hub 
			index[i] = nearest_hub
			#The city is linked to the hub 
			flow_copy[nearest_hub-1] = flow_copy[i]+flow_copy[nearest_hub-1]
			flow_copy = flow_copy.drop(columns = i)
		for i in range(self.cities):
			#in this loop the cost of transport and delivery is determined. 
			flowss = list(flow_copy.iloc[i])
			to_hub = index[i] - 1 
			prices = list(cost_copy[to_hub])
			total_packages = sum(flowss)
			transfer_cost = sum([int(flowss[i])*int(prices[i]) for i in range(len(flowss))])
			distribution_cost = self.package_cost[to_hub][i+1]*math.ceil(total_packages/bus_capactity)*distribution_factor*total_packages
			cost+= distribution_cost + transfer_cost
		return cost


		print(flow_copy)



test = parcel(file_name) 
print(test.calculate_cost([6]))
