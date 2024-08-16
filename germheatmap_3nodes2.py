#the list has been selected in according to the mean heatmap
UC_germs=['411471', '1965549', '1501230', '457393', '1834082', '1273686', '93975', '1965550', '745368', '411483', '1834109', '1965648', '1890373']
CD_germs=['515619', '411469', '1531', '818', '1834109', '1203554', '1077285', '1776047', '1574262', '1834105', '1965639', '1965550', '53378', '411471', '1965581', '301302', '2022527', '745368', '47678', '1690268', '1834112', '93974', '997894', '536231', '1891969', '1739298', '1776046', '1834196', '1150298', '1232460', '1776045', '411483', '762967', '537011']
non_germs=['1965588', '515619', '146922', '1834109', '1965549', '1776047', '693988', '1834091', '592028', '46503', '1965639', '53378', '665953', '1834088', '1965581', '301302', '1408428', '285514', '745368', '2044307', '1834112', '1834089', '1891969', '1776046', '1150298', '411483', '537011']

all_germs=[]
all_germs.extend(UC_germs)
all_germs.extend(CD_germs)
all_germs.extend(non_germs)
all_germs=sorted(list(set(all_germs)))
print(all_germs)


def matcher(str1):
	matcher1=re.match(r'\(\'([^\']*)\',\s*(\d+)',str1)
	float_str=matcher1.group(1)
	integer_str=matcher1.group(2)
	return float_str,integer_str

sicks=['UC','CD','non']
import os,csv,re
import warnings
warnings.filterwarnings('ignore')

def toconnect(label,list1):
    new_list1=[]
    for i in list1:
        germs=label.split(',')
        for j in range(len(i)):
            if i[j]==0:
                continue
            else:
                if j==0:
                    for n in range(i[j]):
                        new_list1.append((germs[0],germs[1]))
                elif j==1:
                    for n in range(i[j]):
                        new_list1.append((germs[1],germs[2]))
                elif j==2:
                    for n in range(i[j]):
                        new_list1.append((germs[0],germs[2]))
    return new_list1

all_structure=[]
all_nodes=[]
all_patient_info=[]
all_info=dict()

for sick in  sicks:
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
					struture: list[list[int]]=[]
					for string_idx in range(1,len(lines)):
						float_str,integer=matcher(lines[string_idx])
						edge_value_list=list(map(lambda x:int(float(x)),float_str.split(' ')))
						for i in range(int(integer)):
							struture.append(edge_value_list)
					dict1[lines[0]]=toconnect(lines[0],struture)

			for node_comb in dict1.keys():
				all_nodes.append(node_comb)
			all_patient_info.append(dict1)

			if patient_name not in all_info.keys():
				all_info[patient_name]=[]
			all_info[patient_name].append(dict1)

import pandas as pd
from collections import Counter
#检验每一种细菌的计数
UC_germs_df=pd.DataFrame(columns=all_germs,index=all_germs[::-1])
CD_germs_df=pd.DataFrame(columns=all_germs,index=all_germs[::-1])
non_germs_df=pd.DataFrame(columns=all_germs,index=all_germs[::-1])

all_info2_non=[]
for i in all_info.keys():
    label=i.split('_')[1]
    if label!='non':
        continue
    for dict1 in all_info[i]:
        a=dict1.values()
        for n in a:
            all_info2_non.extend(n)

all_info2_UC=[]
for i in all_info.keys():
    label=i.split('_')[1]
    if label!='UC':
        continue
    for dict1 in all_info[i]:
        a=dict1.values()
        for n in a:
            all_info2_UC.extend(n)

all_info2_CD=[]
for i in all_info.keys():
    label=i.split('_')[1]
    if label!='CD':
        continue
    for dict1 in all_info[i]:
        a=dict1.values()
        for n in a:
            all_info2_CD.extend(n)

counter_non=Counter(all_info2_non)
counter_UC=Counter(all_info2_UC)
counter_CD=Counter(all_info2_CD)

for i in UC_germs_df.columns:
    for j in UC_germs_df.index:
        if i==j:
            continue
        else:
            UC_germs_df.loc[j,i]=counter_UC[(i,j)]
            UC_germs_df.loc[i,j]=counter_UC[(i,j)]

for i in CD_germs_df.columns:
    for j in CD_germs_df.index:
        if i==j:
            continue
        else:
            CD_germs_df.loc[j,i]=counter_CD[(i,j)]
            CD_germs_df.loc[i,j]=counter_CD[(i,j)]


for i in non_germs_df.columns:
    for j in non_germs_df.index:
        if i==j:
            continue
        else:
            non_germs_df.loc[j,i]=counter_non[(i,j)]
            non_germs_df.loc[i,j]=counter_non[(i,j)]

import seaborn as sns
import matplotlib.pyplot as plt
UC_germs_df =UC_germs_df.apply(pd.to_numeric, errors='coerce')
UC_germs_df.fillna(0,inplace=True)
CD_germs_df=CD_germs_df.apply(pd.to_numeric, errors='coerce')
CD_germs_df.fillna(0,inplace=True)
non_germs_df=non_germs_df.apply(pd.to_numeric, errors='coerce')
non_germs_df.fillna(0,inplace=True)
print(non_germs_df.columns)

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
middle_value = (non_germs_df.max() - non_germs_df.min()) / 2
color = sm.to_rgba(middle_value)

plt.figure(figsize=(20,10))
plt.xticks(fontsize=5, rotation=45)
plt.yticks(fontsize=5, rotation=0)
plt.gcf().autofmt_xdate()
plt.title('non_germs with 3 nodes')
sns.heatmap(non_germs_df, annot=False, fmt=".2f", cmap=cmap)
plt.show()