import networkx as nx
import pandas as pd
import numpy as np
import openpyxl
import pytest
import math
from anytree import Node, RenderTree
import matplotlib.pyplot as plt


def create_graph_from_excel_file(absolutePath):
    data = pd.read_excel(absolutePath, index_col=0)
    result_graph = nx.Graph()
    # print("\n", data, "\n")
    # list from 'A' to 'G'
    all_nodes_names = data.columns
    # Creating the nodes
    result_graph.add_nodes_from(all_nodes_names)
    # print(result_graph)
    edges_tables = []
    # for every node
    for row in data.iterrows():
        node_name = row[0]
        all_nodes_edges_weight = row[1]
        # for every edge inside the node row
        for index, weight in enumerate(all_nodes_edges_weight):
            # i have to check it's not Nan or 0
            if not math.isnan(weight) and weight != 0:
                edges_tables.append((node_name, all_nodes_names[index], {'weight': weight}))

    # a table we can convert to edges
    result_graph.add_edges_from(edges_tables)
    print("\nAll graph edges =", result_graph.edges, "\n")
    print("edge between A and B = \n", result_graph.edges['B', 'A'], "\n")

    return result_graph


def greedy_algorithm_init(graph: nx.Graph, root_name: str):
    greedy_tree = nx.DiGraph()
    available_nodes = list(graph.nodes)
    greedy_tree.add_node(root_name , distance=0 , real_name="A")
    print("The root distance =", greedy_tree.nodes[root_name]['distance'], '\n')
    print("The root successors : ", graph.adj[root_name])
    root_adjacents=graph.adj[root_name]
    # the shortest way : so we will use il our next mouvement
    best_node= None
    for node_name,node_details in root_adjacents.items():
        edge_weight=node_details['weight']
        print("node name =", node_name, "\n")
        print("edge weight =", edge_weight ,"\n")
        greedy_tree.add_node(node_name , distance=edge_weight)
        greedy_tree.add_weighted_edges_from([(root_name , node_name , edge_weight)])
        if best_node is None  or best_node[1] > edge_weight:
            best_node=(node_name , edge_weight)
    available_nodes.remove(root_name)
    greedy_algorithm_recursive(graph , greedy_tree , best_node[0] , available_nodes)
    # nx.draw(greedy_tree, with_labels=True, font_weight='bold')
    # plt.show()


def greedy_algorithm_recursive(graph : nx.Graph , greedy_tree : nx.DiGraph , best_node_name : str , available_nodes : list  ):
    print("best node name =", best_node_name)
    available_nodes.remove(best_node_name)
    print("available_nodes =", available_nodes)