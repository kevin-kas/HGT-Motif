import re
import os,csv,re
import warnings
from collections import Counter
warnings.filterwarnings('ignore')

non_sick_reason=['1834105', '1776047', '1776045', '81858', '665953', '449673', '53378', '411483', '1965588', '1834088', '622312', '1965550', '46503', '301302', '537011']
CD_sick_reason=['1531', '1834196', '1574262', '1965581', '997894', '536231', '1834112', '762967', '1852381', '411483', '745368', '1965550', '1776046', '1203554']
UC_sick_reason=['1776047', '1834112', '536231', '665953', '1834088', '411483', '745368', '1776046', '1891970', '46503', '537011']

print(len(non_sick_reason))
print(len(CD_sick_reason))
print(len(UC_sick_reason))

non_special=['411483,411483,1965550,1965588 with structure9', '411483,411483,1965550,1965588 with structure5', '411483,411483,1965550,1965588 with structure3', '411483,411483,1965550,1965588 with structure11', '411483,411483,1965550,1965588 with structure8', '301302,622312,1834105,1834105 with structure1', '301302,622312,1834105,1834105 with structure0', '301302,622312,1834105,1834105 with structure3', '301302,622312,1834105,1834105 with structure11', '301302,622312,1834105,1834105 with structure14', '301302,622312,1834105,1834105 with structure8','46503,665953,1834088,1834088 with structure11', '46503,665953,1834088,1834088 with structure14', '46503,665953,1834088,1834088 with structure8', '81858,449673,665953,1834088 with structure1', '81858,449673,665953,1834088 with structure13', '81858,449673,665953,1834088 with structure7', '81858,449673,665953,1834088 with structure5', '81858,449673,665953,1834088 with structure12', '81858,449673,665953,1834088 with structure11', '81858,449673,665953,1834088 with structure6', '81858,449673,665953,1834088 with structure2', '53378,537011,537011,1776047 with structure1', '53378,537011,537011,1776047 with structure13', '53378,537011,537011,1776047 with structure7', '53378,537011,537011,1776047 with structure5', '53378,537011,537011,1776047 with structure12', '53378,537011,537011,1776047 with structure4', '53378,537011,537011,1776047 with structure3', '53378,537011,537011,1776047 with structure11', '53378,537011,537011,1776047 with structure6', '53378,537011,537011,1776047 with structure16', '53378,537011,537011,1776047 with structure2', '537011,537011,1776045,1776047 with structure1', '537011,537011,1776045,1776047 with structure0', '537011,537011,1776045,1776047 with structure9', '537011,537011,1776045,1776047 with structure5', '537011,537011,1776045,1776047 with structure3', '537011,537011,1776045,1776047 with structure11', '537011,537011,1776045,1776047 with structure16', '537011,537011,1776045,1776047 with structure14', '537011,537011,1776045,1776047 with structure15', '537011,537011,1776045,1776047 with structure8']
CD_special=['411483,411483,1965550,1965581 with structure8', '1531,997894,1776046,1834196 with structure7', '1531,997894,1776046,1834196 with structure5', '1531,997894,1776046,1834196 with structure4', '1531,997894,1776046,1834196 with structure3', '1531,997894,1776046,1834196 with structure16', '1531,997894,1776046,1834196 with structure14', '1531,997894,1776046,1834196 with structure15', '762967,1203554,1574262,1852381 with structure1', '762967,1203554,1574262,1852381 with structure0', '762967,1203554,1574262,1852381 with structure7', '762967,1203554,1574262,1852381 with structure9', '762967,1203554,1574262,1852381 with structure4', '762967,1203554,1574262,1852381 with structure12', '762967,1203554,1574262,1852381 with structure3', '762967,1203554,1574262,1852381 with structure6', '762967,1203554,1574262,1852381 with structure2', '762967,1203554,1574262,1852381 with structure14', '762967,1203554,1574262,1852381 with structure15', '762967,1203554,1574262,1852381 with structure8','762967,1203554,1574262,1852381 with structure8', '411483,536231,745368,1834112 with structure1', '411483,536231,745368,1834112 with structure13', '411483,536231,745368,1834112 with structure9', '411483,536231,745368,1834112 with structure4', '411483,536231,745368,1834112 with structure16']
UC_special=['411483,536231,745368,1834112 with structure16', '411483,411483,745368,1834088 with structure1', '411483,411483,745368,1834088 with structure0', '411483,411483,745368,1834088 with structure5', '411483,411483,745368,1834088 with structure12', '411483,411483,745368,1834088 with structure4', '411483,411483,745368,1834088 with structure3', '411483,411483,745368,1834088 with structure6', '411483,411483,745368,1834088 with structure2', '411483,411483,745368,1834088 with structure15', '411483,411483,745368,1834088 with structure8', '537011,537011,1776047,1891970 with structure1', '537011,537011,1776047,1891970 with structure0', '537011,537011,1776047,1891970 with structure9', '537011,537011,1776047,1891970 with structure5', '537011,537011,1776047,1891970 with structure12', '537011,537011,1776047,1891970 with structure3', '537011,537011,1776047,1891970 with structure11', '537011,537011,1776047,1891970 with structure14', '537011,537011,1776047,1891970 with structure8', '537011,537011,537011,1891970 with structure13', '537011,537011,537011,1891970 with structure2', '537011,537011,1891970,1891970 with structure0', '537011,537011,1891970,1891970 with structure8', '537011,537011,1891970,1891970 with structure3', '537011,537011,537011,1776047 with structure2', '537011,537011,1776046,1776047 with structure1', '537011,537011,1776046,1776047 with structure13', '537011,537011,1776046,1776047 with structure0', '537011,537011,1776046,1776047 with structure9', '537011,537011,1776046,1776047 with structure5', '537011,537011,1776046,1776047 with structure3', '537011,537011,1776046,1776047 with structure11', '537011,537011,1776046,1776047 with structure16', '537011,537011,1776046,1776047 with structure14', '537011,537011,1776046,1776047 with structure8', '46503,665953,1834088,1834088 with structure9']



def change_structure(nodes,structure_id):
	structure=[]
	if structure_id==0:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[0],nodes[3]))

	elif structure_id==1:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[1],nodes[3]))

	elif structure_id==2:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[2],nodes[3]))

	elif structure_id==3:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[0],nodes[3]))
		structure.append((nodes[1],nodes[2]))

	elif structure_id==4:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[0],nodes[3]))
		structure.append((nodes[2],nodes[3]))

	elif structure_id==5:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[1],nodes[2]))
		structure.append((nodes[1],nodes[3]))

	elif structure_id==6:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[1],nodes[2]))
		structure.append((nodes[2],nodes[3]))

	elif structure_id==7:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[1],nodes[3]))
		structure.append((nodes[2],nodes[3]))

	elif structure_id==8:
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[0],nodes[3]))
		structure.append((nodes[1],nodes[3]))

	elif structure_id==9:
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[0],nodes[3]))
		structure.append((nodes[1],nodes[3]))

	elif structure_id==10:
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[0],nodes[3]))
		structure.append((nodes[2],nodes[3]))

	elif structure_id==11:
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[1],nodes[2]))
		structure.append((nodes[1],nodes[3]))

	elif structure_id==12:
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[1],nodes[2]))
		structure.append((nodes[2],nodes[3]))

	elif structure_id==13:
		structure.append((nodes[0],nodes[2]))
		structure.append((nodes[1],nodes[3]))
		structure.append((nodes[2],nodes[3]))

	elif structure_id==14:
		structure.append((nodes[0],nodes[3]))
		structure.append((nodes[1],nodes[2]))
		structure.append((nodes[1],nodes[3]))

	elif structure_id==15:
		structure.append((nodes[0],nodes[3]))
		structure.append((nodes[1],nodes[2]))
		structure.append((nodes[2],nodes[3]))

	elif structure_id==16:
		structure.append((nodes[0],nodes[3]))
		structure.append((nodes[1],nodes[3]))
		structure.append((nodes[2],nodes[3]))
	return structure


all_structure_non=[]
for i in non_special:
	label=int(i.split(' with ')[1].split('structure')[1])
	nodes=list(map(str,i.split(' with ')[0].split(',')))
	structure=change_structure(nodes,label)
	all_structure_non.extend(structure)
# print(all_structure_non)

all_structure_UC=[]
for i in UC_special:
	label=int(i.split(' with ')[1].split('structure')[1])
	nodes=list(map(str,i.split(' with ')[0].split(',')))
	structure=change_structure(nodes,label)
	all_structure_UC.extend(structure)
print(all_structure_UC)

all_structure_CD=[]
for i in CD_special:
	label=int(i.split(' with ')[1].split('structure')[1])
	nodes=list(map(str,i.split(' with ')[0].split(',')))
	structure=change_structure(nodes,label)
	all_structure_CD.extend(structure)
print(all_structure_CD)

#===============================================================================================================#

#UC x轴 +UC内容
import pandas as pd
num=0
UC_df_with_UC=pd.DataFrame(columns=UC_sick_reason,index=UC_sick_reason[::-1])
# UC_df_with_UC=UC_df_with_UC.fillna(0)
for i in all_structure_UC:
	if i[0] in UC_sick_reason and i[1] in UC_sick_reason and i[0] in UC_sick_reason and i[1] in UC_sick_reason:
		UC_df_with_UC.loc[i[0],i[1]]=1
		UC_df_with_UC.loc[i[1],i[0]]=1
	else:
		continue

#UC x轴 +CD内容
UC_df_with_CD=pd.DataFrame(columns=UC_sick_reason,index=UC_sick_reason[::-1])
# UC_df_with_CD=UC_df_with_CD.fillna(0)
for i in all_structure_CD:
	if i[0] in CD_sick_reason and i[1] in CD_sick_reason and i[0] in UC_sick_reason and i[1] in UC_sick_reason:
		UC_df_with_CD.loc[i[0],i[1]]=1
		UC_df_with_CD.loc[i[1],i[0]]=1
	else:
		continue

#UC x轴 +non内容
UC_df_with_non=pd.DataFrame(columns=UC_sick_reason,index=UC_sick_reason[::-1])
# UC_df_with_non=UC_df_with_non.fillna(0)
for i in all_structure_non:
	if i[0] in non_sick_reason and i[1] in non_sick_reason and i[0] in UC_sick_reason and i[1] in UC_sick_reason:
		UC_df_with_non.loc[i[0],i[1]]=1
		UC_df_with_non.loc[i[1],i[0]]=1
	else:
		continue


#CD x轴 +UC内容
CD_df_with_UC=pd.DataFrame(columns=CD_sick_reason,index=CD_sick_reason[::-1])
# CD_df_with_UC=CD_df_with_UC.fillna(0)
for i in all_structure_UC:
	if i[0] in CD_sick_reason and i[1] in CD_sick_reason and i[0] in UC_sick_reason and i[1] in UC_sick_reason:
		CD_df_with_UC.loc[i[0],i[1]]=1
		CD_df_with_UC.loc[i[1],i[0]]=1
	else:
		continue

#CD x轴 +CD内容
CD_df_with_CD=pd.DataFrame(columns=CD_sick_reason,index=CD_sick_reason[::-1])
# CD_df_with_CD=CD_df_with_CD.fillna(0)
for i in all_structure_CD:
	if i[0] in CD_sick_reason and i[1] in CD_sick_reason and i[0] in CD_sick_reason and i[1] in CD_sick_reason:
		CD_df_with_CD.loc[i[0],i[1]]=1
		CD_df_with_CD.loc[i[1],i[0]]=1
	else:
		continue

#CD x轴 +non内容
CD_df_with_non=pd.DataFrame(columns=CD_sick_reason,index=CD_sick_reason[::-1])
# CD_df_with_non=CD_df_with_non.fillna(0)
for i in all_structure_non:
	if i[0] in CD_sick_reason and i[1] in CD_sick_reason and i[0] in non_sick_reason and i[1] in non_sick_reason:
		CD_df_with_non.loc[i[0],i[1]]=1
		CD_df_with_non.loc[i[1],i[0]]=1
	else:
		continue

#non x轴 +UC内容
non_df_with_UC=pd.DataFrame(columns=non_sick_reason,index=non_sick_reason[::-1])
# non_df_with_UC=non_df_with_UC.fillna(0)
for i in all_structure_UC:
	if i[0] in non_sick_reason and i[1] in non_sick_reason and i[0] in UC_sick_reason and i[1] in UC_sick_reason:
		non_df_with_UC.loc[i[0],i[1]]=1
		non_df_with_UC.loc[i[1],i[0]]=1
	else:
		continue

#non x轴 +CD内容
non_df_with_CD=pd.DataFrame(columns=non_sick_reason,index=non_sick_reason[::-1])
# non_df_with_CD=non_df_with_CD.fillna(0)
for i in all_structure_CD:
	if i[0] in non_sick_reason and i[1] in non_sick_reason and i[0] in CD_sick_reason and i[1] in CD_sick_reason:
		non_df_with_CD.loc[i[0],i[1]]=1
		non_df_with_CD.loc[i[1],i[0]]=1
	else:
		continue

#non x轴 +non内容
non_df_with_non=pd.DataFrame(columns=non_sick_reason,index=non_sick_reason[::-1])
# non_df_with_non=non_df_with_non.fillna(0)
for i in all_structure_non:
	if i[0] in non_sick_reason and i[1] in non_sick_reason and i[0] in non_sick_reason and i[1] in non_sick_reason:
		non_df_with_non.loc[i[0],i[1]]=1
		non_df_with_non.loc[i[1],i[0]]=1
	else:
		continue


import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(16,16))
non_df_with_non.fillna(0,inplace=True)
non_df_with_CD.fillna(0,inplace=True)
non_df_with_UC.fillna(0,inplace=True)
CD_df_with_CD.fillna(0,inplace=True)
CD_df_with_non.fillna(0,inplace=True)
CD_df_with_UC.fillna(0,inplace=True)
UC_df_with_UC.fillna(0,inplace=True)
UC_df_with_non.fillna(0,inplace=True)
UC_df_with_CD.fillna(0,inplace=True)

sns.heatmap(CD_df_with_UC,annot=False,fmt='.2f',cmap='Blues',cbar=False)
plt.title('CD with UC')
plt.yticks(rotation=45)
plt.show()