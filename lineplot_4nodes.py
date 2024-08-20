import os,csv,re
import random
import warnings
from collections import Counter
import networkx as nx
warnings.filterwarnings('ignore')

bool1=lambda x:True if x!=0 else False
def canonical_form(Graph):
	labes=nx.weisfeiler_lehman_graph_hash(Graph)
	adj_list={n:list(Graph.neighbors(n)) for n in Graph.nodes()}
	return labes,adj_list

def getnum(str1):
	if str1[0]=='C':
		num=int(str1.split('C')[2])
	else:
		num=int(str1.split('C')[1])
	return num

def toGraph(structure):
	new_structure=[]
	new_structure2=[]
	for i in range(len(structure)):
		new_structure.append(list(map(bool1,structure[i])))
	for i in new_structure:
		if i == [True, True, True, False, False, False]:
			new_structure2.append('structure0')
		elif i == [True, True, False, False, True, False]:
			new_structure2.append('structure1')
		elif i == [True, True, False, False, False, True]:
			new_structure2.append('structure2')
		elif i == [True, False, True, True, False, False]:
			new_structure2.append('structure3')
		elif i == [True, False, True, False, False, True]:
			new_structure2.append('structure4')
		elif i == [True, False, False, True, True, False]:
			new_structure2.append('structure5')
		elif i == [True, False, False, True, False, True]:
			new_structure2.append('structure6')
		elif i == [True, False, False, False, True, True]:
			new_structure2.append('structure7')
		elif i == [False, True, True, True, False, False]:
			new_structure2.append('structure8')
		elif i == [False, True, True, False, True, False]:
			new_structure2.append('structure9')
		elif i == [False, True, True, False, False, True]:
			new_structure2.append('structure10')
		elif i == [False, True, False, True, True, False]:
			new_structure2.append('structure11')
		elif i == [False, True, False, True, False, True]:
			new_structure2.append('structure12')
		elif i == [False, True, False, False, True, True]:
			new_structure2.append('structure13')
		elif i == [False, False, True, True, True, False]:
			new_structure2.append('structure14')
		elif i == [False, False, True, True, False, True]:
			new_structure2.append('structure15')
		elif i == [False, False, True, False, True, True]:
			new_structure2.append('structure16')
	return new_structure2

def key1(str):
	num=''
	for i in str:
		if i.isdigit():
			num+=i

def matcher(str1):
	matcher1=re.match(r'\(\'([^\']*)\',\s*(\d+)',str1)
	float_str=matcher1.group(1)
	integer_str=matcher1.group(2)
	return float_str,integer_str


all_nodes=[]
all_patient_info=[]
all_info=dict()

sicks=['UC','CD','non']
for sick in sicks:
	for patient_name in os.listdir('4nodes_info_for_plot'):
		if patient_name.split('_')[1]!=sick:
			continue
		table_folder=os.path.join('4nodes_info_for_plot', patient_name)
		for info_table in os.listdir(table_folder):
			with open('4nodes_info_for_plot/'+patient_name+'/'+info_table) as f:
				reader=csv.reader(f)
				dict1=dict()
				for lines in reader:
					if lines==[]:
						continue
					structure=[]
					for string_idx in range(1,len(lines)):
						float_str,integer=matcher(lines[string_idx])
						edge_value_list=list(map(lambda x:int(float(x)),float_str.split(' ')))
						for i in range(int(integer)):
							structure.append(edge_value_list)
						dict1[lines[0]]=toGraph(structure)

			for node_cmb in dict1.keys():
				all_nodes.extend(node_cmb)
			all_patient_info.append(dict1)

			if patient_name not in all_info.keys():
				all_info[patient_name]=[]
			all_info[patient_name].append(dict1)

# for i in all_info:
# 	print(i)
# 	for j in all_info[i]:
# 		print(j)

all_time=[]
list_dir=os.listdir('4nodes_info_for_plot')
for i in list_dir:
	path1=os.path.join('4nodes_info_for_plot', i)
	for j in os.listdir(path1):
		time=j.split('.')[0]
		all_time.append(time)

#将all_info中的数据里面所有的节点组合+结构提取出来
num=0
patient_time_info=[]
for i in all_info.keys():
	#首先先生成各种结构
	list1=[]
	for j in all_info[i]:
		node_cmb_structure = []
		for k in j.keys():
			for l in j[k]:
				node_cmb_structure.append(k+' with '+l)
		list1.append(dict(Counter(node_cmb_structure).most_common(20)))
		patient_time_info.append(dict(Counter(node_cmb_structure).most_common(20)))

time_dict=dict()
for i in range(len(all_time)):
	time_dict[all_time[i]]=patient_time_info[i]
	# print(all_time[i])

all_patient=[]
for i in os.listdir('4nodes_info_for_plot'):
	all_patient.append(i.split('_')[0])

patient_time=dict()
for i in all_patient:
	list1=dict()
	for j in time_dict.keys():
		if i in j:
			list1[j]=(time_dict[j])
	patient_time[i]=list1

def getsum(all_y):
	list1=[0]*len(all_y[0])
	for i in all_y:
		for j in range(len(i)):
			list1[j]+=i[j]
	return list1

import matplotlib.pyplot as plt
#绘制每一个患者不同时间的折线图
for patient in patient_time.keys():
	print(patient)
	#画出不同时间的折线
	x=list(patient_time[patient].keys())
	x=sorted(x,key=lambda x:getnum(x))
	all_node2=[]

	for timepoint in patient_time[patient].keys():
		list1=[0]*len(patient_time[patient])
		#获取全部的节点和structure的组合
		all_node2.extend(list(patient_time[patient][timepoint].keys()))
	all_node3=list(set(all_node2))
	#统计每一个字典中的节点和structure的组合在时间点中的数量
	all_y=[[] for i in range(len(all_node3))]
	for index in range(len(all_node3)):
		for timepoint2 in patient_time[patient].keys():
			if all_node3[index] in list(patient_time[patient][timepoint2].keys()):
				all_y[index].append(patient_time[patient][timepoint2][all_node3[index]])
			else:
				all_y[index].append(0)

	#绘制折线图
	for i in range(len(all_node3)):
		plt.plot(x,all_y[i],label=all_node3[i])
		print(all_y[i])
	print("=================================")
	plt.title("Patient structure plot "+patient)
	plt.xticks(rotation=45)
	plt.show()
	plt.close()

#绘制每一个患者不同时间的折线图
for patient in patient_time.keys():
	print(patient)
	#画出不同时间的折线
	x=list(patient_time[patient].keys())
	x=sorted(x,key=lambda x:getnum(x))
	all_node2=[]

	for timepoint in patient_time[patient].keys():
		list1=[0]*len(patient_time[patient])
		#获取全部的节点和structure的组合
		all_node2.extend(list(patient_time[patient][timepoint].keys()))
	all_node3=list(set(all_node2))
	#统计每一个字典中的节点和structure的组合在时间点中的数量
	all_y=[[] for i in range(len(all_node3))]
	for index in range(len(all_node3)):
		for timepoint2 in patient_time[patient].keys():
			if all_node3[index] in list(patient_time[patient][timepoint2].keys()):
				all_y[index].append(patient_time[patient][timepoint2][all_node3[index]])
			else:
				all_y[index].append(0)

	#绘制折线图
	plt.plot(x,getsum(all_y))
	print("=================================")
	plt.title("Patient sum plot "+patient)
	plt.xticks(rotation=45)
	plt.show()
	plt.close()