import warnings
warnings.filterwarnings("ignore")
CD_special=['818,93974,1690268 with structure1', '818,93974,1690268 with structure3', '818,93974,1690268 with structure2', '818,93974,1690268 with structure4', '818,47678,93974 with structure1', '818,47678,93974 with structure3', '818,47678,93974 with structure2', '818,47678,93974 with structure4', '818,818,93974 with structure1', '818,818,93974 with structure4', '818,818,93974 with structure2', '818,818,93974 with structure3', '818,93974,1739298 with structure1', '818,93974,1739298 with structure3', '818,93974,1739298 with structure2', '818,93974,1739298 with structure4', '818,93974,1077285 with structure1', '818,93974,1077285 with structure3', '818,93974,1077285 with structure2', '818,93974,1077285 with structure4', '818,93974,93974 with structure1', '818,93974,93974 with structure3', '818,93974,93974 with structure2', '997894,1776046,1834196 with structure1', '997894,1776046,1834196 with structure3', '997894,1776046,1834196 with structure2', '997894,1776046,1834196 with structure4', '1531,997894,1776046 with structure3', '762967,1203554,1574262 with structure1', '762967,1203554,1574262 with structure3', '762967,1203554,1574262 with structure2', '762967,1203554,1574262 with structure4', '997894,1232460,1776046 with structure1', '997894,1232460,1776046 with structure4', '997894,1232460,1776046 with structure2', '536231,745368,1834112 with structure2', '411483,536231,1834112 with structure2']
UC_special=[ '301302,515619,1776047 with structure3', '301302,515619,1776047 with structure2', '301302,515619,1776047 with structure4', '537011,537011,1834109 with structure1', '537011,537011,1834109 with structure3', '537011,537011,1834109 with structure2', '537011,537011,1834109 with structure4', '537011,537011,2044307 with structure3', '537011,537011,2044307 with structure2', '537011,537011,2044307 with structure4', '537011,1834112,2022527 with structure1', '537011,1834112,2022527 with structure4', '537011,1834112,2022527 with structure2', '537011,1834112,2022527 with structure3', '537011,537011,2022527 with structure1', '537011,537011,2022527 with structure3', '537011,537011,1891970 with structure1', '537011,537011,1891970 with structure4', '537011,537011,1891970 with structure2', '537011,537011,1891970 with structure3', '537011,537011,1776047 with structure3', '537011,537011,1776047 with structure4', '537011,1891970,1891970 with structure1', '53378,537011,537011 with structure1', '53378,537011,537011 with structure3', '53378,537011,537011 with structure2', '53378,537011,537011 with structure4', '53378,537011,1776047 with structure1', '53378,537011,1776047 with structure3', '53378,537011,1776047 with structure2', '53378,537011,1776047 with structure4', '537011,537011,1776045 with structure1', '537011,537011,1776045 with structure3', '537011,537011,1776045 with structure2', '301302,515619,1834089 with structure1', '301302,515619,1834089 with structure3', '301302,515619,1834089 with structure2', '411483,745368,1834091 with structure1', '411483,745368,1834091 with structure3', '411483,745368,1834091 with structure2', '411483,745368,1834091 with structure4', '301302,1150298,1834112 with structure1', '301302,1150298,1834112 with structure4', '301302,1150298,1834112 with structure3','537011,1834088,2022527 with structure1', '537011,1834088,2022527 with structure3', '537011,1834088,2022527 with structure2', '537011,1834088,2022527 with structure4', '2022527,2022527,2022527 with structure1']
non_special=[ '411483,745368,1834089 with structure1', '411483,745368,1834089 with structure3', '411483,745368,1834089 with structure2', '411483,745368,1834089 with structure4', '46503,665953,1834088 with structure2', '665953,1834088,1834088 with structure1', '285514,537011,1776047 with structure3', '537011,1776047,1776047 with structure1', '537011,1776047,1776047 with structure4', '537011,1776046,1776047 with structure1', '537011,592028,1776047 with structure2', '146922,537011,1776047 with structure3', '411483,745368,745368 with structure3']

def change_structure(nodes,structure_id):
	structure=[]
	if structure_id==1:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[1],nodes[2]))
		structure.append((nodes[0],nodes[2]))
	elif structure_id==2:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[1],nodes[2]))
	elif structure_id==3:
		structure.append((nodes[0],nodes[1]))
		structure.append((nodes[1],nodes[2]))
	elif structure_id==4:
		structure.append((nodes[1],nodes[2]))
		structure.append((nodes[0],nodes[2]))
	return structure

non_sick_reason=['146922', '1776046', '1776047', '1834088', '1834089', '285514', '411483', '46503', '537011', '592028', '665953', '745368']
CD_sick_reason=['1077285', '1203554', '1232460', '1531', '1574262', '1690268', '1739298', '1776046', '1834112', '1834196', '411483', '47678', '536231', '745368', '762967', '818', '93974', '997894']
UC_sick_reason=['1150298', '1776045', '1776047', '1834088', '1834089', '1834091', '1834109', '1834112', '1891970', '2022527', '2044307', '301302', '411483', '515619', '53378', '537011', '745368']


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

sns.heatmap(non_df_with_UC,annot=False,fmt='.2f',cmap='Blues',cbar=False)
plt.title('non with UC')
plt.yticks(rotation=45)
plt.show()