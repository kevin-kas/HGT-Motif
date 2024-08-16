import os,csv,re
import networkx as nx
import random
import math
import warnings

warnings.filterwarnings('ignore')

bool1=lambda x:True if x!=0 else False

def canonical_form(Graph):
    labes=nx.weisfeiler_lehman_graph_hash(Graph)
    adj_list={n:list(Graph.neighbors(n)) for n in Graph.nodes()}
    return labes,adj_list

#获取全部的病人名字，这个作为上面表的x轴
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
        if i==[True,False,True]:
            new_structure2.append('structure1')
        elif i==[False,True,True]:
            new_structure2.append('structure2')
        elif i==[True,True,False]:
            new_structure2.append('structure3')
        elif i==[True,True,True]:
            new_structure2.append('structure4')
    return new_structure2

list_dir1=os.listdir('IBD_DetailedCSV_15_3')
for i in list_dir1:
    label=i.split('_')[1]
    if label=='UC':
        UC_patient.append(i)
    elif label=='CD':
        CD_patient.append(i)
    else:
        non_patient.append(i)

patient_names.extend(CD_patient)
patient_names.extend(UC_patient)
patient_names.extend(non_patient)

#==============================================================#
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
for sick in sicks:
    for patient_name in os.listdir('IBD_DetailedCSV_15_3'):
        if patient_name.split('_')[1]!=sick:
            continue
        table_folder=os.path.join('IBD_DetailedCSV_15_3', patient_name)
        for info_table in os.listdir(table_folder):
            with open('IBD_DetailedCSV_15_3/'+patient_name+'/'+info_table) as f:
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
for i in range(100):
    color_list.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

#从color_list中选取len(germ_name)个颜色
color_list=random.sample(color_list,len(germ_name))

color_dict=dict()
for idx in range(len(germ_name)):
    color_dict[germ_name[idx]]=color_list[idx]

#制造上面的图的x轴
node_structure=dict()
for i in useful_nodes:
    node_structure[i]=[]
    for j in all_info.keys():
        for k in all_info[j]:
            if i in k.keys():
                node_structure[i].extend(list(k[i]))
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
        #patient folder是一个字典合集，有多少CSV就有多少k
        node_cmb,structure_type=i.split(' with ')
        for k in range(len(patient_folder)):
            if node_cmb in patient_folder[k]:
                nums[k]=patient_folder[k][node_cmb].count(structure_type)
            else:
                continue
        if i=='537011,537011,537011 with structure1' and j=='H4001_CD':
            continue
        df.loc[j,i]=math.ceil(sum(nums)/len(nums))

#补充df的均值，按照疾病来分类
#获取全部的sum
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
sum_df = sum_df.apply(pd.to_numeric, errors='coerce')
sum_df.fillna(0, inplace=True)

cluster_matrix=sum_df.transpose()
#==========================================================================#聚类信息
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(cluster_matrix), index=cluster_matrix.index, columns=cluster_matrix.columns)

# 确定K值
# 这里需要根据实际情况使用肘部法则确定K值
k = 3  # 假设我们选择2作为聚类数

# 执行K-Means聚类
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(df_scaled)
cluster_matrix['Cluster'] = clusters

# 查看聚类结果
cluster0=[]
cluster1=[]
cluster2=[]
for index,row in cluster_matrix.iterrows():
    if row['Cluster']==0:
        cluster0.append(row.name)
    elif row['Cluster']==1:
        cluster1.append(row.name)
    elif row['Cluster']==2:
        cluster2.append(row.name)

new_x_axis=[]
new_x_axis.extend(cluster0)
new_x_axis.extend(cluster1)
new_x_axis.extend(cluster2)
new_x_axis=['411483,745368,745368 with structure1', '411483,745368,745368 with structure2', '411483,745368,745368 with structure4', '411471,411483,745368 with structure1', '411471,411483,745368 with structure3', '411471,411483,745368 with structure2', '411471,411483,745368 with structure4', '411483,411483,745368 with structure4', '411483,411483,745368 with structure3', '411483,411483,1965549 with structure1', '411483,411483,1965549 with structure4', '411483,745368,1650663 with structure1', '411483,745368,1650663 with structure3', '411483,745368,1650663 with structure2', '428128,428128,428128 with structure1', '411483,745368,1965648 with structure1', '411483,745368,1965648 with structure4', '411483,745368,1965648 with structure2', '411483,745368,1965648 with structure3', '411471,745368,745368 with structure1', '411471,745368,745368 with structure3', '411471,745368,745368 with structure2', '411471,745368,745368 with structure4', '411483,745368,1834112 with structure1', '411483,745368,1834112 with structure3', '411483,745368,1834112 with structure2', '411483,745368,1834112 with structure4', '411483,411483,1965588 with structure1', '411483,411483,1965588 with structure3', '411483,411483,1965588 with structure2', '411483,411483,1965588 with structure4', '411483,411483,1965648 with structure1', '411483,411483,1965648 with structure3', '411483,411483,1965648 with structure2', '411483,411483,1965648 with structure4', '411471,411483,411483 with structure1', '411471,411483,411483 with structure3', '411471,411483,411483 with structure2', '411471,411483,411483 with structure4', '411483,745368,1965588 with structure1', '411483,745368,1965588 with structure4', '411483,745368,1965588 with structure3', '818,93974,1891969 with structure1', '818,93974,1891969 with structure3', '818,93974,1891969 with structure2', '818,93974,1891969 with structure4', '411483,411483,1965581 with structure1', '411483,411483,1965581 with structure3', '411483,411483,1965581 with structure2', '411483,411483,1965581 with structure4', '93975,457393,1890373 with structure1', '93975,457393,1890373 with structure3', '93975,457393,1890373 with structure2', '93975,457393,1890373 with structure4', '693988,693988,1408428 with structure1', '693988,693988,1408428 with structure4', '693988,693988,1408428 with structure2', '693988,693988,1408428 with structure3', '411483,411483,1965550 with structure1', '411483,411483,1965550 with structure3', '411483,411483,1965550 with structure2', '411483,411483,1965550 with structure4', '411483,745368,1965581 with structure1', '411483,745368,1965581 with structure3', '411483,745368,1965581 with structure4', '411483,745368,1965655 with structure1', '411483,745368,1965549 with structure1', '411483,745368,1965549 with structure3', '411483,745368,1965549 with structure2', '411483,745368,1965549 with structure4', '411483,411483,1965655 with structure1', '411483,411483,1965655 with structure3', '411483,411483,1965655 with structure2', '411483,411483,1965655 with structure4', '301302,515619,1891969 with structure1', '301302,515619,1891969 with structure4', '301302,515619,1891969 with structure2', '301302,515619,1891969 with structure3', '411483,411483,411483 with structure1', '53378,301302,536231 with structure1', '53378,301302,515619 with structure1', '53378,301302,515619 with structure3', '53378,301302,515619 with structure2', '411483,411483,1965551 with structure1', '411483,411483,1965551 with structure4', '411483,411483,1965551 with structure2', '411483,411483,1965551 with structure3', '411483,411483,1965639 with structure1', '411483,411483,1965639 with structure3', '411483,411483,1965639 with structure2', '411483,411483,1965639 with structure4', '411483,745368,1834109 with structure1', '411483,745368,1834109 with structure4', '411483,745368,1834109 with structure2', '411483,745368,1834109 with structure3', '411483,745368,1965550 with structure1', '411483,745368,1965550 with structure3',  '411483,411483,1834109 with structure1', '411483,411483,1834109 with structure3', '411483,411483,1834109 with structure2', '411483,411483,1834109 with structure4','57043,536231,622312 with structure1', '717959,1033731,1965631 with structure1', '717959,1033731,1965631 with structure3', '717959,1033731,1965631 with structure2', '717959,1033731,1965631 with structure4', '717959,1033732,1965650 with structure1', '717959,1033732,1965650 with structure3', '717959,1033732,1965650 with structure2', '717959,1033732,1965650 with structure4', '1273686,1501230,1834082 with structure1', '1273686,1501230,1834082 with structure4', '1273686,1501230,1834082 with structure2','411469,1150298,1834105 with structure2', '818,93974,1690268 with structure1', '818,93974,1690268 with structure3', '818,93974,1690268 with structure2', '818,93974,1690268 with structure4', '818,47678,93974 with structure1', '818,47678,93974 with structure3', '818,47678,93974 with structure2', '818,47678,93974 with structure4', '818,818,93974 with structure1', '818,818,93974 with structure4', '818,818,93974 with structure2', '818,818,93974 with structure3', '818,93974,1739298 with structure1', '818,93974,1739298 with structure3', '818,93974,1739298 with structure2', '818,93974,1739298 with structure4', '818,93974,1077285 with structure1', '818,93974,1077285 with structure3', '818,93974,1077285 with structure2', '818,93974,1077285 with structure4', '818,93974,93974 with structure1', '818,93974,93974 with structure3', '818,93974,93974 with structure2', '997894,1776046,1834196 with structure1', '997894,1776046,1834196 with structure3', '997894,1776046,1834196 with structure2', '997894,1776046,1834196 with structure4', '1531,997894,1776046 with structure3', '762967,1203554,1574262 with structure1', '762967,1203554,1574262 with structure3', '762967,1203554,1574262 with structure2', '762967,1203554,1574262 with structure4', '997894,1232460,1776046 with structure1', '997894,1232460,1776046 with structure4', '997894,1232460,1776046 with structure2', '536231,745368,1834112 with structure2', '411483,536231,1834112 with structure2', '301302,515619,1776047 with structure1', '301302,515619,1776047 with structure3', '301302,515619,1776047 with structure2', '301302,515619,1776047 with structure4', '537011,537011,1834109 with structure1', '537011,537011,1834109 with structure3', '537011,537011,1834109 with structure2', '537011,537011,1834109 with structure4', '537011,537011,2044307 with structure3', '537011,537011,2044307 with structure2', '537011,537011,2044307 with structure4', '537011,1834112,2022527 with structure1', '537011,1834112,2022527 with structure4', '537011,1834112,2022527 with structure2', '537011,1834112,2022527 with structure3', '537011,537011,2022527 with structure1', '537011,537011,2022527 with structure3', '537011,537011,1891970 with structure1', '537011,537011,1891970 with structure4', '537011,537011,1891970 with structure2', '537011,537011,1891970 with structure3', '537011,537011,1776047 with structure3', '537011,537011,1776047 with structure4', '537011,1891970,1891970 with structure1', '53378,537011,537011 with structure1', '53378,537011,537011 with structure3', '53378,537011,537011 with structure2', '53378,537011,537011 with structure4', '53378,537011,1776047 with structure1', '53378,537011,1776047 with structure3', '53378,537011,1776047 with structure2', '53378,537011,1776047 with structure4', '537011,537011,1776045 with structure1', '537011,537011,1776045 with structure3', '537011,537011,1776045 with structure2', '301302,515619,1834089 with structure1', '301302,515619,1834089 with structure3', '301302,515619,1834089 with structure2', '411483,745368,1834091 with structure1', '411483,745368,1834091 with structure3', '411483,745368,1834091 with structure2', '411483,745368,1834091 with structure4', '301302,1150298,1834112 with structure1', '301302,1150298,1834112 with structure4', '301302,1150298,1834112 with structure3','537011,1834088,2022527 with structure1', '537011,1834088,2022527 with structure3', '537011,1834088,2022527 with structure2', '537011,1834088,2022527 with structure4', '2022527,2022527,2022527 with structure1', '301302,1834089,1834109 with structure1', '411483,745368,1834089 with structure1', '411483,745368,1834089 with structure3', '411483,745368,1834089 with structure2', '411483,745368,1834089 with structure4', '46503,665953,1834088 with structure2', '665953,1834088,1834088 with structure1', '285514,537011,1776047 with structure3', '537011,1776047,1776047 with structure1', '537011,1776047,1776047 with structure4', '537011,1776046,1776047 with structure1', '537011,592028,1776047 with structure2', '146922,537011,1776047 with structure3', '411483,745368,745368 with structure3', '301302,411479,1834112 with structure2', '301302,1150298,1834112 with structure2', '537011,537011,537011 with structure1', '537011,537011,2044307 with structure1', '537011,537011,1776047 with structure1', '537011,537011,1776047 with structure2', '411483,411483,745368 with structure1', '411483,411483,745368 with structure2', '622312,1834105,1834105 with structure1']
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
        if i=='537011,537011,537011 with structure1' and j=='H4001_CD':
            continue
        new_dataframe.loc[j,i]=math.ceil(sum(nums)/len(nums))


new_x_axis=['411483,745368,745368 with structure1', '411483,745368,745368 with structure2', '411483,745368,745368 with structure4', '411471,411483,745368 with structure1', '411471,411483,745368 with structure3', '411471,411483,745368 with structure2', '411471,411483,745368 with structure4', '411483,411483,745368 with structure4', '411483,411483,745368 with structure3', '411483,411483,1965549 with structure1', '411483,411483,1965549 with structure4', '411483,745368,1650663 with structure1', '411483,745368,1650663 with structure3', '411483,745368,1650663 with structure2', '428128,428128,428128 with structure1', '411483,745368,1965648 with structure1', '411483,745368,1965648 with structure4', '411483,745368,1965648 with structure2', '411483,745368,1965648 with structure3', '411471,745368,745368 with structure1', '411471,745368,745368 with structure3', '411471,745368,745368 with structure2', '411471,745368,745368 with structure4', '411483,745368,1834112 with structure1', '411483,745368,1834112 with structure3', '411483,745368,1834112 with structure2', '411483,745368,1834112 with structure4', '411483,411483,1965588 with structure1', '411483,411483,1965588 with structure3', '411483,411483,1965588 with structure2', '411483,411483,1965588 with structure4', '411483,411483,1965648 with structure1', '411483,411483,1965648 with structure3', '411483,411483,1965648 with structure2', '411483,411483,1965648 with structure4', '411471,411483,411483 with structure1', '411471,411483,411483 with structure3', '411471,411483,411483 with structure2', '411471,411483,411483 with structure4', '411483,745368,1965588 with structure1', '411483,745368,1965588 with structure4', '411483,745368,1965588 with structure3', '818,93974,1891969 with structure1', '818,93974,1891969 with structure3', '818,93974,1891969 with structure2', '818,93974,1891969 with structure4', '411483,411483,1965581 with structure1', '411483,411483,1965581 with structure3', '411483,411483,1965581 with structure2', '411483,411483,1965581 with structure4', '93975,457393,1890373 with structure1', '93975,457393,1890373 with structure3', '93975,457393,1890373 with structure2', '93975,457393,1890373 with structure4', '693988,693988,1408428 with structure1', '693988,693988,1408428 with structure4', '693988,693988,1408428 with structure2', '693988,693988,1408428 with structure3', '411483,411483,1965550 with structure1', '411483,411483,1965550 with structure3', '411483,411483,1965550 with structure2', '411483,411483,1965550 with structure4', '411483,745368,1965581 with structure1', '411483,745368,1965581 with structure3', '411483,745368,1965581 with structure4', '411483,745368,1965655 with structure1', '411483,745368,1965549 with structure1', '411483,745368,1965549 with structure3', '411483,745368,1965549 with structure2', '411483,745368,1965549 with structure4', '411483,411483,1965655 with structure1', '411483,411483,1965655 with structure3', '411483,411483,1965655 with structure2', '411483,411483,1965655 with structure4', '301302,515619,1891969 with structure1', '301302,515619,1891969 with structure4', '301302,515619,1891969 with structure2', '301302,515619,1891969 with structure3', '411483,411483,411483 with structure1', '53378,301302,536231 with structure1', '53378,301302,515619 with structure1', '53378,301302,515619 with structure3', '53378,301302,515619 with structure2', '411483,411483,1965551 with structure1', '411483,411483,1965551 with structure4', '411483,411483,1965551 with structure2', '411483,411483,1965551 with structure3', '411483,411483,1965639 with structure1', '411483,411483,1965639 with structure3', '411483,411483,1965639 with structure2', '411483,411483,1965639 with structure4', '411483,745368,1834109 with structure1', '411483,745368,1834109 with structure4', '411483,745368,1834109 with structure2', '411483,745368,1834109 with structure3', '411483,745368,1965550 with structure1', '411483,745368,1965550 with structure3',  '411483,411483,1834109 with structure1', '411483,411483,1834109 with structure3', '411483,411483,1834109 with structure2', '411483,411483,1834109 with structure4','57043,536231,622312 with structure1', '717959,1033731,1965631 with structure1', '717959,1033731,1965631 with structure3', '717959,1033731,1965631 with structure2', '717959,1033731,1965631 with structure4', '717959,1033732,1965650 with structure1', '717959,1033732,1965650 with structure3', '717959,1033732,1965650 with structure2', '717959,1033732,1965650 with structure4', '1273686,1501230,1834082 with structure1', '1273686,1501230,1834082 with structure4', '1273686,1501230,1834082 with structure2','411469,1150298,1834105 with structure2', '818,93974,1690268 with structure1', '818,93974,1690268 with structure3', '818,93974,1690268 with structure2', '818,93974,1690268 with structure4', '818,47678,93974 with structure1', '818,47678,93974 with structure3', '818,47678,93974 with structure2', '818,47678,93974 with structure4', '818,818,93974 with structure1', '818,818,93974 with structure4', '818,818,93974 with structure2', '818,818,93974 with structure3', '818,93974,1739298 with structure1', '818,93974,1739298 with structure3', '818,93974,1739298 with structure2', '818,93974,1739298 with structure4', '818,93974,1077285 with structure1', '818,93974,1077285 with structure3', '818,93974,1077285 with structure2', '818,93974,1077285 with structure4', '818,93974,93974 with structure1', '818,93974,93974 with structure3', '818,93974,93974 with structure2', '997894,1776046,1834196 with structure1', '997894,1776046,1834196 with structure3', '997894,1776046,1834196 with structure2', '997894,1776046,1834196 with structure4', '1531,997894,1776046 with structure3', '762967,1203554,1574262 with structure1', '762967,1203554,1574262 with structure3', '762967,1203554,1574262 with structure2', '762967,1203554,1574262 with structure4', '997894,1232460,1776046 with structure1', '997894,1232460,1776046 with structure4', '997894,1232460,1776046 with structure2', '536231,745368,1834112 with structure2', '411483,536231,1834112 with structure2', '301302,515619,1776047 with structure1', '301302,515619,1776047 with structure3', '301302,515619,1776047 with structure2', '301302,515619,1776047 with structure4', '537011,537011,1834109 with structure1', '537011,537011,1834109 with structure3', '537011,537011,1834109 with structure2', '537011,537011,1834109 with structure4', '537011,537011,2044307 with structure3', '537011,537011,2044307 with structure2', '537011,537011,2044307 with structure4', '537011,1834112,2022527 with structure1', '537011,1834112,2022527 with structure4', '537011,1834112,2022527 with structure2', '537011,1834112,2022527 with structure3', '537011,537011,2022527 with structure1', '537011,537011,2022527 with structure3', '537011,537011,1891970 with structure1', '537011,537011,1891970 with structure4', '537011,537011,1891970 with structure2', '537011,537011,1891970 with structure3', '537011,537011,1776047 with structure3', '537011,537011,1776047 with structure4', '537011,1891970,1891970 with structure1', '53378,537011,537011 with structure1', '53378,537011,537011 with structure3', '53378,537011,537011 with structure2', '53378,537011,537011 with structure4', '53378,537011,1776047 with structure1', '53378,537011,1776047 with structure3', '53378,537011,1776047 with structure2', '53378,537011,1776047 with structure4', '537011,537011,1776045 with structure1', '537011,537011,1776045 with structure3', '537011,537011,1776045 with structure2', '301302,515619,1834089 with structure1', '301302,515619,1834089 with structure3', '301302,515619,1834089 with structure2', '411483,745368,1834091 with structure1', '411483,745368,1834091 with structure3', '411483,745368,1834091 with structure2', '411483,745368,1834091 with structure4', '301302,1150298,1834112 with structure1', '301302,1150298,1834112 with structure4', '301302,1150298,1834112 with structure3','537011,1834088,2022527 with structure1', '537011,1834088,2022527 with structure3', '537011,1834088,2022527 with structure2', '537011,1834088,2022527 with structure4', '2022527,2022527,2022527 with structure1', '301302,1834089,1834109 with structure1', '411483,745368,1834089 with structure1', '411483,745368,1834089 with structure3', '411483,745368,1834089 with structure2', '411483,745368,1834089 with structure4', '46503,665953,1834088 with structure2', '665953,1834088,1834088 with structure1', '285514,537011,1776047 with structure3', '537011,1776047,1776047 with structure1', '537011,1776047,1776047 with structure4', '537011,1776046,1776047 with structure1', '537011,592028,1776047 with structure2', '146922,537011,1776047 with structure3', '411483,745368,745368 with structure3', '301302,411479,1834112 with structure2', '301302,1150298,1834112 with structure2', '537011,537011,537011 with structure1', '537011,537011,2044307 with structure1', '537011,537011,1776047 with structure1', '537011,537011,1776047 with structure2', '411483,411483,745368 with structure1', '411483,411483,745368 with structure2', '622312,1834105,1834105 with structure1']
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

#======================================================================================#
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
print(list(new_mean_df.columns))
# 现在尝试重新绘制热图
plt.figure(figsize=(20,10))
plt.xticks(fontsize=4, rotation=45)
plt.yticks(fontsize=10, rotation=0)
plt.gcf().autofmt_xdate()
sns.heatmap(new_mean_df, annot=False, fmt=".2f", cmap=cmap)

plt.show()

with open('1.txt','w') as f:
    a=list(new_mean_df.columns)
    for i in a:
        f.write(i)
        f.write('\n')