#对于之前的txt文件做处理，并且以txt文件存起来，这里是一三节点为例子，不考虑点之间的自环
import math
import csv
import os
from collections import Counter
class result:
	def __init__(self):
		self.label=[]
		self.data_column=[]
		self.data=[]
	def clear(self):
		self.label = []
		self.data_column = []
		self.data = []

#找到文件中的最小数字，当里面的
def deal(filename):
	import math
	num2=math.inf
	with open(filename,'r',encoding='utf-8') as f:
		for i in f:
			if "当" in i:
				string1=''
				for j in i:
					if j.isdecimal():
						string1+=j
				num2=0

	# 将文件中所有的信息提取出来包括datafram和节点组合
	ans=[]
	with open(filename,'r',encoding='utf-8') as f:
		list1=[]
		for i in f:
			equel_count=0
			if "当"  in i:
				equel_count+=1
				num2+=1
				if int(num2)==15:
					break
				continue
			if "=" in i:
				equel_count+=1
			if equel_count&1==0:
				if i=='\n':
					continue
				list1.append(i.strip())
			else:
				if list1==[''] or list1==[]:
					continue
				if len(list1)==1:
					continue
				if len(list1)==6:
					list1=list1[1::]
				ans.append(list1[:])
				list1.clear()
	# 进行一种特定的处理，目的是去除掉之前文件中的空格等各种符号
	list2=[]
	for i in ans:
		label = sorted(list(set(list(map(lambda x: int(float(x)), i[0].split())))))
		a=result()
		i=i[1::]
		a.label=label
		list3=[]
		dataframe=[]
		for j in i:
			j=j.replace(' ',',')
			j = j.replace(',,,,,,,,', ',').replace(',,,,,,,', ',').replace(',,,,,,', ',').replace(',,,,,', ',').replace(',,,', ',').replace(',,', ',')
			dataframe.append(j.split(',')[1::])
			list3.append(j.split(',')[0])
		a.data_column=list3
		a.data=dataframe
		list2.append(a)

	# 对于矩阵进行排序，确保矩阵是一个的节点的顺序，这样子可以避免成识别不同的节点组合，如将A-B-C和C-B-A识别为不同的情况，结构存储在dataframe中
	#
	def sorter(a,b):
		list1=list(map(float,a))
		if len(a)==4:
			for i in range(len(a)):
				for j in range(i,len(a)):
					if list1[i]>list1[j] and ((i==1 and j==0) or (j==1 and i==0)):
						list1[i],list1[j]=list1[j],list1[i]
						b[0][0], b[1][1] = b[1][1], b[0][0]
						b[0][2], b[1][2] = b[1][2], b[0][2]
						b[0][3], b[1][3] = b[1][3], b[0][3]
						b[2][0], b[2][1] = b[2][1], b[2][0]
						b[3][0], b[3][1] = b[3][1], b[3][0]

					if list1[i]>list1[j] and ((i==0 and j==2) or (i==2 and j==0)):
						list1[i],list1[j]=list1[j],list1[i]
						b[0][0],b[2][2]=b[2][2],b[0][0]
						b[0][1],b[2][1]=b[2][1],b[0][1]
						b[0][3],b[2][3]=b[2][3],b[0][3]
						b[1][0],b[1][2]=b[1][2],b[1][0]
						b[3][0],b[3][2]=b[3][2],b[3][0]

					if list1[i]>list1[j] and ((i==0 and j==3) or (i==3 and j==0)):
						list1[i],list1[j]=list1[j],list1[i]
						b[0][0],b[3][3]=b[3][3],b[0][0]
						b[0][1],b[3][1]=b[3][1],b[0][1]
						b[0][2],b[3][2]=b[3][2],b[0][2]
						b[1][0],b[1][3]=b[1][3],b[1][0]
						b[2][0],b[2][3]=b[2][3],b[2][0]

					if list1[i]>list1[j] and ((i==1 and j==2) or (i==2 and j==1)):
						list1[i],list1[j]=list1[j],list1[i]
						b[1][1],b[2][2]=b[2][2],b[1][1]
						b[1][0],b[2][0]=b[2][0],b[1][0]
						b[1][3],b[2][3]=b[2][3],b[1][3]
						b[0][1],b[0][2]=b[0][2],b[0][1]
						b[3][1],b[3][2]=b[3][2],b[3][1]


					if list1[i]>list1[j] and ((i==1 and j==3) or (i==3 and j==1)):
						list1[i],list1[j]=list1[j],list1[i]
						b[1][1],b[3][3]=b[3][3],b[1][1]
						b[1][0],b[3][0]=b[3][0],b[1][0]
						b[1][2],b[3][2]=b[3][2],b[1][2]
						b[0][1],b[0][3]=b[0][3],b[0][1]
						b[2][1],b[2][3]=b[2][3],b[2][1]


					if list1[i]>list1[j] and ((i==2 and j==3) or (i==3 and j==2)):
						list1[i],list1[j]=list1[j],list1[i]
						b[2][2],b[3][3]=b[3][3],b[2][2]
						b[2][0],b[3][0]=b[3][0],b[2][0]
						b[2][1],b[3][1]=b[3][1],b[2][1]
						b[0][2],b[0][3]=b[0][3],b[0][2]
						b[1][2],b[1][3]=b[1][3],b[1][2]
			return list1,b

		elif len(a)==3:
			for i in range(len(a)):
				for j in range(i, len(a)):
					if list1[i] > list1[j] and ((i == 1 and j == 0) or (j == 1 and i == 0)):
						list1[i], list1[j] = list1[j], list1[i]
						b[0][0], b[1][1] = b[1][1], b[0][0]
						b[0][2], b[1][2] = b[1][2], b[0][2]
						b[2][0], b[2][1] = b[2][1], b[2][0]

					if list1[i] > list1[j] and ((i == 2 and j == 0) or (j == 2 and i == 0)):
						list1[i], list1[j] = list1[j], list1[i]
						b[0][0], b[2][2] = b[2][2], b[0][0]
						b[0][1], b[2][1] = b[2][1], b[0][1]
						b[1][0], b[1][2] = b[1][2], b[1][0]

					if list1[i] > list1[j] and ((i == 2 and j == 1) or (j == 2 and i == 1)):
						list1[i], list1[j] = list1[j], list1[i]
						b[1][1], b[2][2] = b[2][2], b[1][1]
						b[1][0], b[2][0] = b[2][0], b[1][0]
						b[0][1], b[0][2] = b[0][2], b[0][1]

			return list1, b

		elif len(a)==2:
			list1 = list(map(float, a.split()))
			for i in range(len(a)):
				for j in range(i, len(a)):
					if list1[i] > list1[j]:
						list1[i], list1[j] = list1[j], list1[i]
						b[0][0], b[1][1] = b[1][1], b[0][0]
			return list1, b
	#
	class motif:
		def __init__(self, motif_label, column_data, data):
			self.motif_label = motif_label
			self.column_data = column_data
			self.data = data
	#进行替换，同时将dataframe转换为list来存储，每个位置来表示对应的dataframe
	list3=[]
	for i in list2:
		a1=sorter(i.data_column,i.data)
		new_motif_label,new_data_column,new_data = i.label,a1[0],a1[1]
		k=[new_data[0][1],new_data[0][2],new_data[0][3],new_data[1][2],new_data[1][3],new_data[2][3]]#这是第二个类中所存储的边的边的边权
		for i in range(len(k)):
			if k[i]=='NaN':
				k[i]='0.0'
		a=motif(new_motif_label,a1[0],k)
		list3.append(a)

	#
	dict1=dict()
	for i in list3:
		label = ','.join(list(map(str, list(map(int, i.column_data)))))
		if label in dict1.keys():
			dict1[label].append(i.data)
		else:
			dict1[label]=[i.data]

	list4=[]
	for i in dict1.keys():
		new_list1=[]
		new_list2=[]
		for j in dict1[i]:
			new_list1.append(' '.join(j))
		dict2=dict(Counter(new_list1).most_common())

		for j in dict2.keys():
			new_list2.append((j,dict2[j]))
		new_list2.insert(0,i)
		list4.append(new_list2)

	import csv
	with open(filename.replace('txt', 'csv'), 'w', encoding='utf-8') as f:
		writer = csv.writer(f)
		for i in list4:
			writer.writerow(i)

#批量化处理特定位置的文件
list_dir=os.listdir('tocsv4nodes')
for i in list_dir:
	deal('tocsv4nodes/'+i)
	print(i)
