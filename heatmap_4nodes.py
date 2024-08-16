import os,csv,re
import random
import math
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

bool1=lambda x:True if x!=0 else False
def canonical_form(Graph):
	labes=nx.weisfeiler_lehman_graph_hash(Graph)
	adj_list={n:list(Graph.neighbors(n)) for n in Graph.nodes()}
	return labes,adj_list

patient_names=[]
UC_patient=[]
CD_patient=[]
non_patient=[]

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

list_dir1=os.listdir('IBD_DetailedCSV_15_4')
for i in list_dir1:
	label=i.split('_')[1]
	if label=='UC':
		UC_patient.append(i)
	elif label=='CD':
		CD_patient.append(i)
	else:
		non_patient.append(i)

patient_names.extend(UC_patient)
patient_names.extend(CD_patient)
patient_names.extend(non_patient)

all_structure=[]
all_nodes=[]
all_patient_info=[]
all_info=dict()

def matcher(str1):
	matcher1=re.match(r'\(\'([^\']*)\',\s*(\d+)',str1)
	float_str=matcher1.group(1)
	integer_str=matcher1.group(2)
	return float_str,integer_str

sicks=['UC','CD','non']
for sick in  sicks:
	for patient_name in os.listdir('IBD_DetailedCSV_15_4'):
		if patient_name.split('_')[1]!=sick:
			continue
		table_folder=os.path.join('IBD_DetailedCSV_15_4', patient_name)
		for info_table in os.listdir(table_folder):
			with open('IBD_DetailedCSV_15_4/'+patient_name+'/'+info_table) as f:
				reader=csv.reader(f)
				dict1=dict()
				for lines in reader:
					if lines==[]:
						continue
					struture=[]
					for string_idx in range(1,len(lines)):
						float_str,integer=matcher(lines[string_idx])
						edge_value_list=list(map(lambda x:int(float(x)),float_str.split(' ')))
						for i in range(int(integer)):
							struture.append(edge_value_list)
					dict1[lines[0]]=toGraph(struture)

			for node_comb in dict1.keys():
				all_nodes.append(node_comb)
			all_patient_info.append(dict1)

			if patient_name not in all_info.keys():
				all_info[patient_name]=[]
			all_info[patient_name].append(dict1)


node_freq=dict()
for i in all_nodes:
	num=0
	for j in all_patient_info:
		if i in j.keys():
			num+=1
	node_freq[i]=num

useful_nodes=[]
for i in node_freq.keys():
	if node_freq[i]<3:
		continue
	else:
		useful_nodes.append(i)

germ_name=[]
for i in useful_nodes:
	nodess=list(map(int,i.split(',')))
	germ_name.extend(nodess)

germ_name=list(set(germ_name))

color_list=[]
for i in range(400):
	color_list.append((random.randint(0,255)/255,random.randint(0,255)/255,random.randint(0,255)/255))

color_list=random.sample(color_list,len(germ_name))

color_dict=dict()
for idx in range(len(germ_name)):
	color_dict[germ_name[idx]]=color_list[idx]

node_structure=dict()
for i in useful_nodes:
	node_structure[i]=[]
	for j in all_info.keys():
		for k in all_info[j]:
			if i in k.keys():
				node_structure[i].extend(k[i])
	node_structure[i]=list(set(node_structure[i]))


x_axis=[]
for i in node_structure:
	for j in node_structure[i]:
		x_axis.append(i+' with '+j)

import pandas as pd
df=pd.DataFrame(index=patient_names,columns=x_axis)

for i in df.columns:
	for j in df.index:
		patient_folder=all_info[j]
		nums=[0]*len(patient_folder)
		node_cmb,struture_type=i.split(' with ')
		for k in range(len(patient_folder)):
			if node_cmb in patient_folder[k]:
				nums[k]=patient_folder[k][node_cmb].count(struture_type)
			else:
				continue
			df.loc[j,i]=math.ceil(sum(nums)/len(nums))

sum_df=pd.DataFrame(columns=x_axis)

#获取UC的sum
UC_df=df.loc[UC_patient]
UC_sum_series=UC_df.sum()
sum_df.loc['UC_sum']=UC_sum_series
#获取CD的sum
CD_df=df.loc[CD_patient]
CD_sum_series=CD_df.sum()
sum_df.loc['CD_sum']=CD_sum_series
#获取non的sum
non_df=df.loc[non_patient]
non_sum_series=non_df.sum()
sum_df.loc['non_sum']=non_sum_series

import pandas as pd
sum_df=sum_df.apply(pd.to_numeric,errors='ignore')
sum_df.fillna(0,inplace=True)

cluster_matrix=sum_df.transpose()
#===========================================================================#
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(cluster_matrix), index=cluster_matrix.index, columns=cluster_matrix.columns)

kmeans = KMeans(n_clusters=3)
clusters=kmeans.fit_predict(df_scaled)
cluster_matrix['cluster']=clusters

cluster0=[]
cluster1=[]
cluster2=[]

for index,row in cluster_matrix.iterrows():
	if row['cluster']==0:
		cluster0.append(index)
	elif row['cluster']==1:
		cluster1.append(index)
	else:
		cluster2.append(index)

new_x_axis=[]
new_x_axis.extend(cluster0)
new_x_axis.extend(cluster1)
new_x_axis.extend(cluster2)
new_x_axis=['411471,411483,411483,745368 with structure7', '411471,411483,411483,745368 with structure5', '411483,411483,411483,745368 with structure1', '411483,411483,411483,745368 with structure0', '411483,411483,411483,745368 with structure7', '411483,411483,411483,745368 with structure9', '411483,411483,411483,745368 with structure4', '411483,411483,411483,745368 with structure16', '411483,411483,411483,745368 with structure2', '411471,411483,745368,745368 with structure1', '411471,411483,745368,745368 with structure13', '411471,411483,745368,745368 with structure0', '411471,411483,745368,745368 with structure7', '411471,411483,745368,745368 with structure9', '411471,411483,745368,745368 with structure4', '411471,411483,745368,745368 with structure12', '411471,411483,745368,745368 with structure3', '411471,411483,745368,745368 with structure11', '411471,411483,745368,745368 with structure16', '411471,411483,745368,745368 with structure14', '411471,411483,745368,745368 with structure15', '411471,411483,745368,745368 with structure8', '411483,411483,745368,745368 with structure3', '411483,411483,745368,745368 with structure8', '411471,411483,411483,745368 with structure0', '411471,411483,411483,745368 with structure9', '411471,411483,411483,745368 with structure12', '411471,411483,411483,745368 with structure11', '411471,411483,411483,745368 with structure8', '411483,411483,745368,1965588 with structure1', '411483,411483,745368,1965588 with structure13', '411483,411483,745368,1965588 with structure9', '411483,411483,745368,1965588 with structure5', '411483,411483,745368,1965588 with structure4', '411483,411483,745368,1965588 with structure12', '411483,411483,745368,1965588 with structure11', '411483,411483,745368,1965588 with structure2', '411483,411483,745368,1965588 with structure14', '411483,411483,745368,1965588 with structure15', '411471,411483,745368,1965588 with structure1', '411471,411483,745368,1965588 with structure9', '411471,411483,745368,1965588 with structure5', '411471,411483,745368,1965588 with structure4', '411471,411483,745368,1965588 with structure12', '411471,411483,745368,1965588 with structure3', '411471,411483,745368,1965588 with structure11', '411471,411483,745368,1965588 with structure6', '411471,411483,745368,1965588 with structure2', '411471,411483,745368,1965588 with structure14', '411471,411483,745368,1965588 with structure8', '411483,411483,745368,1965549 with structure1', '411483,411483,745368,1965549 with structure9', '411483,411483,745368,1965549 with structure5', '411483,411483,745368,1965549 with structure12', '411483,411483,745368,1965549 with structure4', '411483,411483,745368,1965549 with structure3', '411483,411483,745368,1965549 with structure11', '411483,411483,745368,1965549 with structure6', '411483,411483,745368,1965549 with structure2', '411483,411483,745368,1965549 with structure14', '411483,411483,745368,1965549 with structure15', '411483,411483,745368,1965549 with structure8', '411483,411483,745368,1891969 with structure1', '411483,411483,745368,1891969 with structure0', '411483,411483,745368,1891969 with structure5', '411483,411483,745368,1891969 with structure9', '411483,411483,745368,1891969 with structure4', '411483,411483,745368,1891969 with structure3', '411483,411483,745368,1891969 with structure11', '411483,411483,745368,1891969 with structure6', '411483,411483,745368,1891969 with structure2', '411483,411483,745368,1891969 with structure14', '411483,411483,745368,1891969 with structure15', '411483,411483,745368,1891969 with structure8', '411483,411483,745368,1965655 with structure1', '411483,411483,745368,1965655 with structure0', '411483,411483,745368,1965655 with structure9', '411483,411483,745368,1965655 with structure5', '411483,411483,745368,1965655 with structure12', '411483,411483,745368,1965655 with structure3', '411483,411483,745368,1965655 with structure11', '411483,411483,745368,1965655 with structure2', '411483,411483,745368,1965655 with structure14', '411483,411483,745368,1965655 with structure15', '411483,411483,745368,1965655 with structure8', '411471,411483,745368,1965648 with structure1', '411471,411483,745368,1965648 with structure0', '411471,411483,745368,1965648 with structure5', '411471,411483,745368,1965648 with structure11', '411471,411483,745368,1965648 with structure6', '411471,411483,745368,1965648 with structure2', '411483,411483,745368,1834112 with structure0', '411483,411483,745368,1834112 with structure4', '411483,411483,745368,1834112 with structure12', '411483,411483,745368,1834112 with structure3', '411483,411483,745368,1834112 with structure6', '411483,411483,745368,1834112 with structure2', '411483,411483,745368,1834112 with structure15', '411483,411483,745368,1834112 with structure8', '411483,411483,745368,1965648 with structure1', '411483,411483,745368,1965648 with structure13', '411483,411483,745368,1965648 with structure7', '411483,411483,745368,1965648 with structure9', '411483,411483,745368,1965648 with structure5', '411483,411483,745368,1965648 with structure12', '411483,411483,745368,1965648 with structure4', '411483,411483,745368,1965648 with structure3', '411483,411483,745368,1965648 with structure11', '411483,411483,745368,1965648 with structure6', '411483,411483,745368,1965648 with structure16', '411483,411483,745368,1965648 with structure2', '411483,411483,745368,1965648 with structure14', '411483,411483,745368,1965648 with structure15', '411483,411483,745368,1965550 with structure12', '411483,411483,745368,1965550 with structure16', '411483,411483,745368,1965550 with structure15', '411483,411483,745368,1965581 with structure13', '411483,411483,745368,1965581 with structure7', '411483,411483,745368,1965581 with structure4', '411483,411483,745368,1965581 with structure12', '411483,411483,745368,1965581 with structure3', '411483,411483,745368,1965581 with structure6', '411483,411483,745368,1965581 with structure16', '411483,411483,745368,1965581 with structure2', '411483,411483,745368,1965581 with structure15', '411483,411483,745368,1965551 with structure1', '411483,411483,745368,1965551 with structure0', '411483,411483,745368,1965551 with structure9', '411483,411483,745368,1965551 with structure5', '411483,411483,745368,1965551 with structure3', '411483,411483,745368,1965551 with structure11', '411483,411483,745368,1965551 with structure16', '411483,411483,745368,1965551 with structure14', '411483,411483,745368,1965551 with structure8', '411483,411483,1965581,1965648 with structure1', '411483,411483,1965581,1965648 with structure0', '411483,411483,1965581,1965648 with structure9', '411483,411483,1965581,1965648 with structure5', '411483,411483,1965581,1965648 with structure3', '411483,411483,1965581,1965648 with structure14', '411483,411483,1965581,1965648 with structure8', '411483,411483,1965550,1965648 with structure1', '411483,411483,1965550,1965648 with structure0', '411483,411483,1965550,1965648 with structure9', '411483,411483,1965550,1965648 with structure3', '411483,411483,1965550,1965648 with structure11', '411483,411483,1965550,1965648 with structure14', '411483,411483,1965550,1965648 with structure15', '411483,411483,1965550,1965648 with structure8', '411483,411483,745368,1965639 with structure1', '411483,411483,745368,1965639 with structure0', '411483,411483,745368,1965639 with structure5', '411483,411483,745368,1965639 with structure9', '411483,411483,745368,1965639 with structure3', '411483,411483,745368,1965639 with structure11', '411483,411483,745368,1965639 with structure16', '411483,411483,745368,1965639 with structure14', '411483,411483,745368,1965639 with structure8', '411483,411483,1965550,1965639 with structure1', '411483,411483,1965550,1965639 with structure0', '411483,411483,1965550,1965639 with structure3', '411483,411483,1965550,1965639 with structure11', '411483,411483,1965550,1965639 with structure14', '411483,411483,1965550,1965639 with structure8', '411483,411483,1965550,1965551 with structure1', '411483,411483,1965550,1965551 with structure0', '411483,411483,1965550,1965551 with structure9', '411483,411483,1965550,1965551 with structure5', '411483,411483,1965550,1965551 with structure3', '411483,411483,1965550,1965551 with structure11', '411483,411483,1965550,1965551 with structure8', '411483,411483,745368,1650663 with structure1', '411483,411483,745368,1650663 with structure0', '411483,411483,745368,1650663 with structure5', '411483,411483,745368,1650663 with structure9', '411483,411483,745368,1650663 with structure12', '411483,411483,745368,1650663 with structure11', '411483,411483,745368,1650663 with structure14', '411483,411483,745368,1650663 with structure8', '411483,411483,1965639,1965648 with structure1', '411483,411483,1965639,1965648 with structure7', '411483,411483,1965639,1965648 with structure0', '411483,411483,1965639,1965648 with structure5', '411483,411483,1965639,1965648 with structure4', '411483,411483,1965639,1965648 with structure3', '411483,411483,1965639,1965648 with structure11', '411483,411483,1965639,1965648 with structure8', '411483,411483,745368,1834109 with structure13', '411483,411483,745368,1834109 with structure5', '411483,411483,745368,1834109 with structure4', '411483,411483,745368,1834109 with structure12', '411483,411483,745368,1834109 with structure3', '411483,411483,745368,1834109 with structure11', '411483,411483,745368,1834109 with structure6', '411483,411483,745368,1834109 with structure2', '411483,411483,745368,1834109 with structure14', '411483,411483,745368,1834109 with structure15', '411483,411483,745368,1834109 with structure8','411483,411483,1965550,1965588 with structure1', '411483,411483,1965550,1965588 with structure0', '411483,411483,1965550,1965588 with structure9', '411483,411483,1965550,1965588 with structure5', '411483,411483,1965550,1965588 with structure3', '411483,411483,1965550,1965588 with structure11', '411483,411483,1965550,1965588 with structure8', '301302,622312,1834105,1834105 with structure1', '301302,622312,1834105,1834105 with structure0', '301302,622312,1834105,1834105 with structure3', '301302,622312,1834105,1834105 with structure11', '301302,622312,1834105,1834105 with structure14', '301302,622312,1834105,1834105 with structure8', '411483,411483,411483,1965581 with structure1', '411483,411483,411483,1965581 with structure13', '411483,411483,411483,1965581 with structure7', '411483,411483,411483,1965581 with structure0', '411483,411483,411483,1965581 with structure9', '411483,411483,411483,1965581 with structure4', '411483,411483,411483,1965581 with structure16', '411483,411483,411483,1965581 with structure2', '411483,411483,1965550,1965581 with structure1', '411483,411483,1965550,1965581 with structure0', '411483,411483,1965550,1965581 with structure9', '411483,411483,1965550,1965581 with structure5', '411483,411483,1965550,1965581 with structure3', '411483,411483,1965550,1965581 with structure11', '411483,411483,1965550,1965581 with structure14', '411483,411483,1965550,1965581 with structure8', '1531,997894,1776046,1834196 with structure7', '1531,997894,1776046,1834196 with structure5', '1531,997894,1776046,1834196 with structure4', '1531,997894,1776046,1834196 with structure3', '1531,997894,1776046,1834196 with structure16', '1531,997894,1776046,1834196 with structure14', '1531,997894,1776046,1834196 with structure15', '762967,1203554,1574262,1852381 with structure1', '762967,1203554,1574262,1852381 with structure0', '762967,1203554,1574262,1852381 with structure7', '762967,1203554,1574262,1852381 with structure9', '762967,1203554,1574262,1852381 with structure4', '762967,1203554,1574262,1852381 with structure12', '762967,1203554,1574262,1852381 with structure3', '762967,1203554,1574262,1852381 with structure6', '762967,1203554,1574262,1852381 with structure2', '762967,1203554,1574262,1852381 with structure14', '762967,1203554,1574262,1852381 with structure15', '762967,1203554,1574262,1852381 with structure8', '411483,536231,745368,1834112 with structure1', '411483,536231,745368,1834112 with structure13', '411483,536231,745368,1834112 with structure9', '411483,536231,745368,1834112 with structure4', '411483,536231,745368,1834112 with structure16', '411483,411483,745368,1834088 with structure1', '411483,411483,745368,1834088 with structure0', '411483,411483,745368,1834088 with structure5', '411483,411483,745368,1834088 with structure12', '411483,411483,745368,1834088 with structure4', '411483,411483,745368,1834088 with structure3', '411483,411483,745368,1834088 with structure6', '411483,411483,745368,1834088 with structure2', '411483,411483,745368,1834088 with structure15', '411483,411483,745368,1834088 with structure8', '537011,537011,1776047,1891970 with structure1', '537011,537011,1776047,1891970 with structure0', '537011,537011,1776047,1891970 with structure9', '537011,537011,1776047,1891970 with structure5', '537011,537011,1776047,1891970 with structure12', '537011,537011,1776047,1891970 with structure3', '537011,537011,1776047,1891970 with structure11', '537011,537011,1776047,1891970 with structure14', '537011,537011,1776047,1891970 with structure8', '537011,537011,537011,1891970 with structure13', '537011,537011,537011,1891970 with structure2', '537011,537011,1891970,1891970 with structure0', '537011,537011,1891970,1891970 with structure8', '537011,537011,1891970,1891970 with structure3', '537011,537011,537011,1776047 with structure2', '537011,537011,1776046,1776047 with structure1', '537011,537011,1776046,1776047 with structure13', '537011,537011,1776046,1776047 with structure0', '537011,537011,1776046,1776047 with structure9', '537011,537011,1776046,1776047 with structure5', '537011,537011,1776046,1776047 with structure3', '537011,537011,1776046,1776047 with structure11', '537011,537011,1776046,1776047 with structure16', '537011,537011,1776046,1776047 with structure14', '537011,537011,1776046,1776047 with structure8', '46503,665953,1834088,1834088 with structure9', '46503,665953,1834088,1834088 with structure11', '46503,665953,1834088,1834088 with structure14', '46503,665953,1834088,1834088 with structure8', '81858,449673,665953,1834088 with structure1', '81858,449673,665953,1834088 with structure13', '81858,449673,665953,1834088 with structure7', '81858,449673,665953,1834088 with structure5', '81858,449673,665953,1834088 with structure12', '81858,449673,665953,1834088 with structure11', '81858,449673,665953,1834088 with structure6', '81858,449673,665953,1834088 with structure2', '53378,537011,537011,1776047 with structure1', '53378,537011,537011,1776047 with structure13', '53378,537011,537011,1776047 with structure7', '53378,537011,537011,1776047 with structure5', '53378,537011,537011,1776047 with structure12', '53378,537011,537011,1776047 with structure4', '53378,537011,537011,1776047 with structure3', '53378,537011,537011,1776047 with structure11', '53378,537011,537011,1776047 with structure6', '53378,537011,537011,1776047 with structure16', '53378,537011,537011,1776047 with structure2', '537011,537011,1776045,1776047 with structure1', '537011,537011,1776045,1776047 with structure0', '537011,537011,1776045,1776047 with structure9', '537011,537011,1776045,1776047 with structure5', '537011,537011,1776045,1776047 with structure3', '537011,537011,1776045,1776047 with structure11', '537011,537011,1776045,1776047 with structure16', '537011,537011,1776045,1776047 with structure14', '537011,537011,1776045,1776047 with structure15', '537011,537011,1776045,1776047 with structure8', '411471,411483,745368,745368 with structure5', '411471,411483,745368,745368 with structure6', '411471,411483,745368,745368 with structure2', '411483,411483,745368,745368 with structure0', '411483,411483,745368,745368 with structure12', '411483,411483,745368,745368 with structure4', '411483,411483,745368,745368 with structure6', '411483,411483,745368,745368 with structure2', '411483,411483,745368,745368 with structure15', '411471,411483,411483,745368 with structure1', '411471,411483,411483,745368 with structure13', '411471,411483,411483,745368 with structure4', '411471,411483,411483,745368 with structure3', '411471,411483,411483,745368 with structure6', '411471,411483,411483,745368 with structure16', '411471,411483,411483,745368 with structure2', '411471,411483,411483,745368 with structure14', '411471,411483,411483,745368 with structure15', '411483,411483,745368,1965588 with structure0', '411483,411483,745368,1965588 with structure3', '411483,411483,745368,1965588 with structure8', '411483,411483,745368,1965549 with structure0', '411483,411483,411483,745368 with structure13', '411483,411483,745368,1965648 with structure0', '411483,411483,745368,1965648 with structure8', '411483,411483,745368,1965550 with structure1', '411483,411483,745368,1965550 with structure0', '411483,411483,745368,1965550 with structure9', '411483,411483,745368,1965550 with structure5', '411483,411483,745368,1965550 with structure3', '411483,411483,745368,1965550 with structure11', '411483,411483,745368,1965550 with structure14', '411483,411483,745368,1965550 with structure8', '411483,411483,745368,1965581 with structure1', '411483,411483,745368,1965581 with structure0', '411483,411483,745368,1965581 with structure9', '411483,411483,745368,1965581 with structure5', '411483,411483,745368,1965581 with structure11', '411483,411483,745368,1965581 with structure14', '411483,411483,745368,1965581 with structure8', '411483,411483,745368,1834109 with structure0','1033732,1965631,1965650,2585118 with structure1', '1033732,1965631,1965650,2585118 with structure13', '1033732,1965631,1965650,2585118 with structure7', '1033732,1965631,1965650,2585118 with structure0', '1033732,1965631,1965650,2585118 with structure9', '1033732,1965631,1965650,2585118 with structure5', '1033732,1965631,1965650,2585118 with structure4', '1033732,1965631,1965650,2585118 with structure12', '1033732,1965631,1965650,2585118 with structure3', '1033732,1965631,1965650,2585118 with structure11', '1033732,1965631,1965650,2585118 with structure6', '1033732,1965631,1965650,2585118 with structure16', '1033732,1965631,1965650,2585118 with structure2', '1033732,1965631,1965650,2585118 with structure14', '1033732,1965631,1965650,2585118 with structure15', '1033732,1965631,1965650,2585118 with structure8', '1531,997894,1776046,1834196 with structure6', '537011,537011,537011,1891970 with structure1', '537011,537011,537011,1891970 with structure7', '537011,537011,537011,1891970 with structure0', '537011,537011,537011,1891970 with structure9', '537011,537011,537011,1891970 with structure4', '537011,537011,537011,1891970 with structure16', '537011,537011,537011,1776047 with structure1', '537011,537011,537011,1776047 with structure13', '537011,537011,537011,1776047 with structure0', '537011,537011,537011,1776047 with structure7', '537011,537011,537011,1776047 with structure9', '537011,537011,537011,1776047 with structure4', '537011,537011,537011,1776047 with structure16']
new_dataframe=pd.DataFrame(columns=new_x_axis,index=patient_names)
for i in new_dataframe.columns:
    for j in new_dataframe.index:
        patient_folder=all_info[j]
        nums=[0]*len(patient_folder)
        #patient folder是一个字典合集，有多少CSV就有多少k
        node_cmb,structure_type=i.split(' with ')

        for k in range(len(patient_folder)):
            if node_cmb in patient_folder[k]:
                nums[k]=patient_folder[k][node_cmb].count(structure_type)
            else:
                continue
        new_dataframe.loc[j,i]=math.ceil(sum(nums)/len(nums))

new_mean_df=pd.DataFrame(columns=new_x_axis)
#获取UC的sum
UC_df=df.loc[UC_patient]
UC_mean_series=UC_df.mean()
new_mean_df.loc['UC_mean']=UC_mean_series
#获取CD的sum
CD_df=df.loc[CD_patient]
CD_mean_series=CD_df.mean()
new_mean_df.loc['CD_mean']=CD_mean_series
#获取non的sum
non_df=df.loc[non_patient]
non_mean_series=non_df.mean()
new_mean_df.loc['non_mean']=non_mean_series

new_mean_df = new_mean_df.apply(pd.to_numeric, errors='coerce')
new_mean_df.fillna(0, inplace=True)
print(new_mean_df)

#========================================================================================#
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
def toone(list1):
	a=[]
	for i in list1:
		list2=[]
		for j in i:
			list2.append(j/255)
		a.append(tuple(list2))
	return a

colors = [(240,240,240),(76,164,162),(54,104,107),(25,49,52)]
colors=toone(colors)
cmap_name = 'my_custom_cmap'
cmap = LinearSegmentedColormap.from_list(cmap_name, colors)
sm = ScalarMappable(cmap=cmap)
middle_value = (new_mean_df.max() - new_mean_df.min()) / 2
color = sm.to_rgba(middle_value)
import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(20,10))
plt.xticks(fontsize=3, rotation=45)
plt.yticks(fontsize=10, rotation=0)
plt.gcf().autofmt_xdate()
sns.heatmap(new_mean_df, annot=False, fmt=".2f", cmap=cmap)
plt.show()
print(list(new_mean_df.columns))
with open('4nodes_x.txt','w') as f:
    a=list(new_dataframe.columns)
    for i in a:
        f.write(i)
        f.write('\n')