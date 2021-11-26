import networkx as nx
import pandas as pd
import numpy as np
import openpyxl
import pytest
import math
from anytree import Node, RenderTree
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
import scipy as sp

levels_colors = ["#000000", "#ff0000", "#00ff00", "#0000ff", "#333", "#eee", "#ffff00"]
node_colors = []


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
    global levels_colors
    global node_colors
    greedy_tree = nx.DiGraph()
    available_nodes = list(graph.nodes)
    available_nodes.remove(root_name)
    greedy_tree.add_node(root_name, distance=0, real_name="A")
    node_colors.append(levels_colors[0])
    print("The root distance =", greedy_tree.nodes[root_name]['distance'], '\n')
    print("The root successors : ", graph.adj[root_name])
    root_adjacents = graph.adj[root_name]
    # the shortest way : so we will use il our next mouvement
    best_node = None
    for node_name, node_details in root_adjacents.items():
        edge_weight = node_details['weight']
        print("node name =", node_name, "\n")
        print("edge weight =", edge_weight, "\n")
        greedy_tree.add_node(node_name, distance=edge_weight)
        node_colors.append(levels_colors[1])
        greedy_tree.add_weighted_edges_from([(root_name, node_name, edge_weight)])
        if best_node is None or best_node[1] > edge_weight:
            best_node = (node_name, edge_weight)
    available_nodes.remove(best_node[0])
    print("\n------------------ RECURSIVE STARTED HERE  !--------------\n")
    greedy_algorithm_recursive(graph, greedy_tree, best_node[0], available_nodes, 2)
    # pos = nx.planar_layout(greedy_tree)
    pos=graphviz_layout(greedy_tree , prog="dot")
    nx.draw(greedy_tree, with_labels=True, font_weight='bold', node_size=1500, alpha=0.5, node_color=node_colors,
            pos=pos)

    plt.show()


def greedy_algorithm_recursive(graph: nx.Graph, greedy_tree: nx.DiGraph, best_node_name: str, available_nodes: list,
                               level: int):
    global levels_colors
    global node_colors
    print("---------- LEVEL = ", level, "-----------")
    best_node_name_in_greedy = best_node_name * (level - 1)  # C....C
    best_node_name_in_graph = best_node_name  # C
    print("best node name in teh graph =", best_node_name_in_graph, "\n")
    print("best node name in greedy tree =", best_node_name_in_greedy, "\n")
    next_adjacents = graph.adj[best_node_name_in_graph]
    best_node_graph = None

    print("available_nodes =", available_nodes)
    for node_name, node_details in next_adjacents.items():
        edge_weight = node_details['weight']
        # we treat only the nodes we didn't treat yet
        if node_name in available_nodes:
            new_distance = greedy_tree.nodes[best_node_name_in_greedy]['distance'] + edge_weight
            greedy_tree.add_node(node_name * level, distance=new_distance)
            node_colors.append(levels_colors[level])
            greedy_tree.add_weighted_edges_from([(best_node_name_in_greedy, node_name * level, edge_weight)])
            if best_node_graph is None or best_node_graph[1] > edge_weight:
                best_node_graph = (node_name, edge_weight)
    print("\nactual node in the greedy sccessors : ", greedy_tree.adj[best_node_name_in_greedy], "\n")
    print("\nBEST NODE =", best_node_graph, "\n")
    available_nodes.remove(best_node_graph[0])
    if len(available_nodes) != 0:
        greedy_algorithm_recursive(graph, greedy_tree, best_node_graph[0], available_nodes, level + 1)
    # else:
    #     print("first part of final = ", greedy_tree.nodes[best_node_graph[0] * level]['distance'], "\n")
    #     print("second part of final =", graph.edges[
    #         best_node_graph[0], 'A']['weight'], "\n")
    #     final_distance = greedy_tree.nodes[best_node_graph[0] * level]['distance'] + graph.edges[
    #         best_node_graph[0], 'A']['weight']
    #     greedy_tree.nodes['A']['distance'] = final_distance
    #     greedy_tree.add_weighted_edges_from([(best_node_graph[0] * (level), 'A', graph.edges[
    #         best_node_graph[0], 'A'])])
