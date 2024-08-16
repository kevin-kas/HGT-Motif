import math
import random

import networkx as nx
import pandas as pd
class Motif:
    def reader(self,filename):
        list1=[]
        csvfile=pd.read_csv(filename,index_col=0)
        for index,row in csvfile.iterrows():
            for column in csvfile.columns:
                value=row[column]
                if isinstance(value,str):
                    value=float(value)
                if isinstance(value,float):
                    if math.isnan(value):
                        continue
                    list1.append((float(index),float(column),float(value)))
        return list1



    def connected_component(self,subgraph):
        subgraph2=subgraph.to_undirected()
        return nx.is_connected(subgraph2)

    def edgesampling(self,edges,n):
        return random.sample(edges,n)

    def get(self,edgelist):
        list1=[]
        num=0
        while True:
            graph=nx.DiGraph()
            graph1=self.edgesampling(edgelist,3)
            graph.add_edge(str(graph1[0][0]), str(graph1[0][1]), weight=float(graph1[0][2]))
            graph.add_edge(str(graph1[1][0]), str(graph1[1][1]), weight=float(graph1[1][2]))
            graph.add_edge(str(graph1[2][0]), str(graph1[2][1]), weight=float(graph1[2][2]))
            if self.connected_component(graph) and len(list(graph.nodes))==4:
                list1.append(graph)
                num+=1
            if num==100000:
                break

        while True:
            graph=nx.DiGraph()
            graph1=self.edgesampling(edgelist,4)
            graph.add_edge(str(graph1[0][0]), str(graph1[0][1]), weight=float(graph1[0][2]))
            graph.add_edge(str(graph1[1][0]), str(graph1[1][1]), weight=float(graph1[1][2]))
            graph.add_edge(str(graph1[2][0]), str(graph1[2][1]), weight=float(graph1[2][2]))
            graph.add_edge(str(graph1[3][0]), str(graph1[3][1]), weight=float(graph1[3][2]))
            if self.connected_component(graph) and len(list(graph.nodes))==4:
                list1.append(graph)
                num+=1
            if num==100000:
                break

        while True:
            graph=nx.DiGraph()
            graph1=self.edgesampling(edgelist,5)
            graph.add_edge(str(graph1[0][0]), str(graph1[0][1]), weight=float(graph1[0][2]))
            graph.add_edge(str(graph1[1][0]), str(graph1[1][1]), weight=float(graph1[1][2]))
            graph.add_edge(str(graph1[2][0]), str(graph1[2][1]), weight=float(graph1[2][2]))
            graph.add_edge(str(graph1[3][0]), str(graph1[3][1]), weight=float(graph1[3][2]))
            graph.add_edge(str(graph1[4][0]), str(graph1[4][1]), weight=float(graph1[4][2]))
            if self.connected_component(graph) and len(list(graph.nodes))==4:
                list1.append(graph)
                num+=1
            if num==100000:
                break

        while True:
            graph=nx.DiGraph()
            graph1=self.edgesampling(edgelist,6)
            graph.add_edge(str(graph1[0][0]), str(graph1[0][1]), weight=float(graph1[0][2]))
            graph.add_edge(str(graph1[1][0]), str(graph1[1][1]), weight=float(graph1[1][2]))
            graph.add_edge(str(graph1[2][0]), str(graph1[2][1]), weight=float(graph1[2][2]))
            graph.add_edge(str(graph1[3][0]), str(graph1[3][1]), weight=float(graph1[3][2]))
            graph.add_edge(str(graph1[4][0]), str(graph1[4][1]), weight=float(graph1[4][2]))
            graph.add_edge(str(graph1[5][0]), str(graph1[5][1]), weight=float(graph1[5][2]))
            if self.connected_component(graph) and len(list(graph.nodes))==4:
                list1.append(graph)
                num+=1
            if num==100000:
                break
        return list1

    def motif(self,filename):
        edgeslist=self.reader(filename)
        motif_res=self.get(edgeslist)
        return motif_res

    def getdata(self,filename):
        list1=[]
        a=self.motif(filename)
        for i in a:
            nodeslist=i.nodes
            edgeslist=i.edges(data=True)

            df=pd.DataFrame(index=nodeslist,columns=nodeslist)
            for j in edgeslist:
                df.loc[j[1],j[0]]=j[2]['weight']
                df.loc[j[0],j[1]]=j[2]['weight']
            list1.append((df,''.join(sorted(list(i.nodes)))))
        return list1

    def getdata2(self,filename):
        a=self.getdata(filename)
        dict1=dict()

        for i in a:
            if i[1] in dict1.keys():
                dict1[i[1]].append(i[0])
            else:
                if i[1][::-1] in dict1.keys():
                    dict1[i[1][::-1]].append(i[0])
                else:
                    dict1[i[1]]=[i[0]]
        list1=[]
        for i in dict1.keys():
            list1.append((i,dict1[i]))
        list1.sort(key =lambda x:len(x[1]),reverse=True)
        dict2=dict()
        for i in range(20):
            dict2[list1[i][0]]=list1[i][1]
        return dict2

import os
from concurrent.futures import ThreadPoolExecutor
def process_file(file,input_folder,output_folder):
       input_file=os.path.join(input_folder,file)
       a=Motif().getdata2(input_file)
       output_file=os.path.join(output_folder,f"{os.path.splitext(file)[0]}.txt")
       with open(output_file,'w') as file1:
           for i,key in enumerate(a.keys(),start=1):
               file1.write(key)
               file1.write("\n")
               file1.write(f"当前有{len(a[key])}个在里面")
               file1.write("\n")
               for j in a[key]:
                   file1.write("\n=====================================\n")
                   file1.write(j.to_string())
                   file1.write("\n=====================================\n")

input_folder='input1'
output_folder='output'

list_dir1=os.listdir(input_folder)
for i in list_dir1:
    list_dir2=os.listdir(os.path.join(input_folder,i))
    for j in list_dir2:
        print(os.path.join(input_folder,i,j))
        print(j)
        print(output_folder)
        process_file(j,os.path.join(input_folder,i),output_folder)
