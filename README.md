# HGT-Motif
This Project is about finding the 3 nodes motif and 4 nodes motif structure in a IBD network structure.
The Input Data is a csvfile which includes a adjacency matrix. This matrix use each germs's Taxon ID as the x-axis and y-axis. The value is horizontal gene transfer intensity. And the project also contain a csv dictionary which include the name and the Taxon ID of each germ.

This project use Python 3.11.9 and Matlab as the main language. And some libraries should be install before started.

1.numpy   version 1.26.4

2.Pandas  version 2.2.1

3.matplotlib version 3.8.4

4.networkx version 3.1

This project also include some python file to deal with the problem.Here is an introduction of each file.
1.Find motif method.
This method use the sampling to find the 3 nodes motif and 4 nodes motif. Input the csv adjacency file and then it will output a txt file with a top20 types of germ combination. Each Germ combination will contain n numbers of 

