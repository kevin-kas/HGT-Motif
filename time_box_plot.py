#首先是UC的box plot
#是用样本M2026
import os
import re
import matplotlib.pyplot as plt
import pandas as pd

def getnum(str1):
	if str1[0]=='C':
		num=int(str1.split('C')[2])
	else:
		num=int(str1.split('C')[1])
	return num

def getboxplot(patient):
	path=os.path.join('3nodes_info_for line_plot', patient)
	list_dir=os.listdir(path)
	import csv
	def matcher(str1):
		matcher1=re.match(r'\(\'([^\']*)\',\s*(\d+)',str1)
		float_str=matcher1.group(1)
		integer_str=matcher1.group(2)
		return float_str,integer_str

	all_sorted_time_info=[]
	for i in list_dir:
		path2=os.path.join(path,i)
		# print(path2)
		with open(path2,'r',encoding='utf-8') as file:
			time_info=[]
			reader=csv.reader(file)
			for line in reader:
				if line==[]:
					continue
				for i in line[1::]:
					float_str,integer_str=matcher(i)
					list1=list(map(lambda x:int(float(x)),float_str.split(' ')))
					list1=[i for i in list1 if i>1 ]
					for i in range(int(integer_str)):
						time_info.extend(list1)

			sorted_time_info=sorted(time_info)
			all_sorted_time_info.append(sorted_time_info)

	def getTimepoint(path):
		list1=[]
		list_dir=os.listdir(path)
		for i in list_dir:
			list1.append(i.split('.')[0])
		return list1
	time_point=time_point=sorted(getTimepoint(path),key=lambda x:getnum(x))

	new_all_sorted_time_info=[]
	for i in all_sorted_time_info:
		a=pd.Series(i)
		Q1=a.quantile(0.25)
		Q3=a.quantile(0.75)
		IQR=Q3-Q1
		lower_bound=Q1-1.5*IQR
		upper_bound=Q3+1.5*IQR
		new_all_sorted_time_info.append(a[(a>=lower_bound)&(a<=upper_bound)])

	data_dict={}
	for i in range(len(new_all_sorted_time_info)):
		data_dict[time_point[i]]=new_all_sorted_time_info[i]

	df=pd.DataFrame(data_dict)
	print(df)
	ax=df.boxplot()
	# plt.figure(figsize=(20,10))
	plt.title(f'Boxplot of the edge value of {patient}',fontweight='bold',fontsize=25)
	plt.xticks(rotation=45,fontweight='bold')
	plt.yticks(fontweight='bold')
	plt.ylabel('Values')
	# plt.savefig(f'boxplot/{patient}')
	plt.show()

import os
list_dir=os.listdir('3nodes_info_for line_plot')
for i in list_dir:
	print(i)
	getboxplot(i)