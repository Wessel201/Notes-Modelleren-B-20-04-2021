import pandas as pd 
import matplotlib.pyplot as plt
import itertools
collection_factor = 3
transfer_factor = 1
distribution_factor = 2 
file_name ='Large.xlsx'
class parcel():
	def __init__(self,file):
		xls = pd.ExcelFile(file)
		self.flow = pd.read_excel(xls, 'w')
		self.flow = self.flow.transpose()
		self.package_cost = pd.read_excel(xls, 'c')
		self.package_cost = self.package_cost.transpose()
		self.hub_cost =[13530] + list(pd.read_excel(xls, 'f')[13530])
		self.cities = len(self.flow.columns)
	def calculate_cost(self,hubs):
		cost = 0
		index = {}
		flow_copy = self.flow
		cost_copy = self.package_cost
		flow_copy = self.flow.copy(deep=True)
		cost_copy = self.package_cost.copy(deep=True)
		cost_copy = cost_copy.take([hub for hub in hubs])
		for i in range(1,self.cities):
			if i+1 in hubs:
				index[i] = i
				cost+= self.hub_cost[i-1]
				continue
			nearest_hub = cost_copy.loc[cost_copy[i] > 0 , i].idxmin()
			cost += cost_copy[i][nearest_hub] * flow_copy[i].sum()*collection_factor
			nearest_hub = nearest_hub 
			index[i] = nearest_hub
			flow_copy[nearest_hub-1] = flow_copy[i]+flow_copy[nearest_hub-1]
			flow_copy = flow_copy.drop(columns = i)
		flow_copy = flow_copy.drop(columns = 0)
		for i in range(self.cities - 1):
			# print('index = ' + str(i))
			flowss = list(flow_copy.iloc[i])
			# print(flowss)
#			print(flowss)
			to_hub = index[i+1] - 1
			prices = list(cost_copy[to_hub])
			# print(prices)
#			print(prices)
			total_packages = sum(flowss)
			transfer_cost = sum([int(flowss[i])*int(prices[i]) for i in range(len(flowss))])
			distribution_cost = self.package_cost[to_hub][i+1]*total_packages*distribution_factor
			# print(distribution_cost)13530
			# print(transfer_cost)
			cost+= distribution_cost + transfer_cost
		return cost
#		print(flow_copy)


test = parcel(file_name) 
#print(test.calculate_cost([3]))
## average = list(test.package_cost.mean().sort_values().index)[1:]
#print(test.calculate_cost([]))
#print(test.calculate_cost([7,10]))
#print(test.calculate_cost([7,10]))
# average = list(test.package_cost.mean().sort_values().index)[:]
# print(average)
# y = []
# x = [] 
# for i in range(1,15):
# for i in range(1,13):
# 	x.append(i)
# 	print(i)
# 	print(average[:i])
# 	y.append(test.calculate_cost(average[:i]))

# plt.plot(x,y)
# plt.show()


test = parcel(file_name) 


# with a single hub we have that that 3 has the lowest cost for collection
def collection_hubs(begin_hubs):
    hubs_lst = begin_hubs
    # start with a single value and let python add a hub if the total value drops
    cost = test.calculate_cost(hubs_lst)
    for itr in range(4):
        for i in range(1,len(pd.read_excel(file_name, "w")+1)):
            if i not in hubs_lst:
                hubs_lst.append(i)
       
            else:
                continue
            
            if test.calculate_cost(hubs_lst) <= cost:
                cost = test.calculate_cost(hubs_lst)
#                print(test.calculate_cost(hubs_lst), cost, hubs_lst)
            else:
                hubs_lst.pop()
    
        
        
        
    return(hubs_lst)
#            return(collection_cost)
#
def collection_minimilization():
    summation_lst = []
    for i in range(1,len(pd.read_excel(file_name, "w")+1)):
        summation_lst.append(collection_hubs([i]))
        
    single_lst = (list(itertools.chain(*summation_lst)))
    
    for nb in range(1,len(pd.read_excel(file_name, "w")+1)):
        print(single_lst.count(nb), "amount of times hub: ", nb)
        
def collection_cost(begin_hubs):
    print(test.calculate_cost(collection_hubs(begin_hubs)),collection_hubs(begin_hubs))
    
       
collection_cost([6,14,1,10,13])     
#collection_minimilization()
#Cost for all hubs is 253074
# total of price 6,14,1 is 120922


            

