import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

import pygraphviz
from networkx.drawing.nx_agraph import to_agraph 

import math
import operator

data_df = pd.read_csv("dataset_708466 .csv")
data_df.head()

G = nx.from_pandas_edgelist(data_df,"Seller","Buyer","Amt",create_using=nx.DiGraph())

cc_dict = nx.algorithms.cluster.clustering(G)
epsilon = 0.5

# Remove nodes with zero cc
cc = [(t[0],t[1]) for t in cc_dict.items() if t[1]!=0]



cluster_count = 0

cc = sorted(cc_dict.items(), key=operator.itemgetter(1), reverse=True)
cluster_dict = {k:None for k in [t[0] for t in cc]}

for i in range(len(cc)):

    print(i,"node")

    curr_node, curr_alpha = cc[i]

    if cluster_dict[curr_node] is not None:
        continue

    n_list = G.neighbors(curr_node)

    nv_list = [t for t in n_list if t in cluster_dict.keys() and cluster_dict[t] is not None]

    minj = None
    minj_val = None

    for j in nv_list:

        count = 0
        total = 0

        this_cluster = [x for x in cluster_dict.keys() if cluster_dict[x]==cluster_dict[j]]

        for c in this_cluster:
            count += 1
            total += math.sqrt(cc[[t[0] for t in cc].index(c)][1])
        avg = total/count

        if abs(curr_alpha**2 - avg) <= epsilon:
            if minj is None:
                minj = j
                minj_val = abs(math.sqrt(curr_alpha) - avg)
            else:
                if abs(math.sqrt(curr_alpha) - avg) < minj_val:
                    minj = j
                    minj_val = abs(math.sqrt(curr_alpha) - avg)

    if minj is not None:
        cluster_dict[curr_node] = cluster_dict[minj]
    
    else:

        cluster_dict[curr_node] = cluster_count
        
        nn_list = [t for t in n_list if t in cluster_dict.keys() and cluster_dict[t] is None]

        for j in nn_list:

            if abs(cc[[t[0] for t in cc].index(j)][1] - curr_alpha) <= epsilon:
                cluster_dict[j] = cluster_count
        
        cluster_count += 1

newdict = {k:[j for j in cluster_dict.keys() if cluster_dict[j]==k] for k in set(cluster_dict.values()) if len([j for j in cluster_dict.keys() if cluster_dict[j]==k])>2 and len([j for j in cluster_dict.keys() if cluster_dict[j]==k])<=5}

cluster_list = newdict.values()

ecIc_ratios = []

cluster_idx = 0
for node_list in cluster_list:
  eC = 0
  iC = 0
  edges = G.edges()
  for edge in edges:
    u = edge[0]
    v = edge[1]
    if u in node_list or v in node_list:
        if (u not in node_list or v not in node_list):
            eC += G[u][v]["Amt"]
        else:
            iC += G[u][v]["Amt"]
  q = iC/eC
  ecIc_ratios.append(q)

count = 0
Gm = nx.from_pandas_edgelist(data_df,"Seller","Buyer","Amt",create_using=nx.MultiDiGraph())
for idx,cluster_id in enumerate(newdict.keys()):
	if len(set(Gm.to_undirected().subgraph(newdict[cluster_id]).edges)) > 2 and not nx.is_directed_acyclic_graph(G.subgraph(newdict[cluster_id])):
		print(count)
		A = to_agraph(Gm.subgraph(newdict[cluster_id])) 
		A.layout('dot')                                                                 
		A.draw(f'multi_{idx}.png')
		count += 1