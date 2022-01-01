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
import  json
import scipy as sp

levels_colors = ["#000000", "#ff0000", "#00ff00", "#0000ff", "#333", "#eee", "#ffff00"]
node_colors = []
complete_tree_edges_lables = dict()
complete_tree_final_distances = list()


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
    greedy_tree.add_node(root_name, distance=0, real_name=root_name)
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
    pos = graphviz_layout(greedy_tree, prog="dot")
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


# For the complete algorithm
def complete_algorithm_init(graph: nx.Graph, root_name: str):
    global levels_colors
    global node_colors
    global complete_tree_edges_lables
    complete_tree = nx.DiGraph()
    available_nodes = list(graph.nodes)
    available_nodes.remove(root_name)
    complete_tree.add_node(root_name, distance=0, real_name=root_name)
    node_colors.append(levels_colors[0])
    print("The root distance =", complete_tree.nodes[root_name]['distance'], '\n')
    print("The root successors : ", graph.adj[root_name])
    root_adjacents = graph.adj[root_name]
    # we execute the recusivite in each children of the root
    for node_name, node_details in root_adjacents.items():
        edge_weight = node_details['weight']
        print("node name =", node_name, "\n")
        print("edge weight =", edge_weight, "\n")
        complete_tree.add_node(node_name, distance=edge_weight, parents=[root_name])
        node_colors.append(levels_colors[1])
        complete_tree.add_weighted_edges_from([(root_name, node_name, edge_weight)])
        complete_tree_edges_lables[(root_name, node_name)] = edge_weight
        print("EDGE LABELS =", complete_tree_edges_lables)
        print("\n------------------ RECURSIVE STARTED HERE  !--------------\n")
        complete_algorithm_recursive(graph, complete_tree, node_name, 2 , root_name)
    pos = graphviz_layout(complete_tree, prog="dot")
    # pos=nx.spiral_layout(complete_tree)
    # plt.figure(figsize=(10,4) , dpi=200)
    fig, ax = plt.subplots()
    nx.draw(complete_tree, with_labels=True, alpha=0.5,
            pos=pos, font_size=8)
    nx.draw_networkx_edge_labels(
        complete_tree, pos,
        edge_labels=complete_tree_edges_lables,
        font_color='red'
    )
    fig.set_size_inches([600, 30])
    plt.savefig("myplot.svg", dpi=200)
    shortestPath = min(complete_tree_final_distances, key=lambda x: x['final_distance'])
    with open('result.txt', 'w') as result_file:
        result_file.write(json.dumps(shortestPath))

    # plt.show()

    return complete_tree


def complete_algorithm_recursive(graph: nx.Graph, complete_tree: nx.DiGraph, actual_node: str, level: int , root_name :str):
    global levels_colors
    global node_colors
    global complete_tree_final_distances
    print("---------- LEVEL = ", level, "-----------")
    print("----------- ACTUAL NODES : ", complete_tree.nodes, "----------")
    if nodeNameCpt(complete_tree.nodes, actual_node * (level - 1)) != 0:
        actual_node_name_in_complete = actual_node * (level - 1) + str(
            nodeNameCpt(complete_tree.nodes, actual_node * (level - 1)) - 1)  # C....C7
    else:
        actual_node_name_in_complete = actual_node * (level - 1)  # C....C
    actual_node_name_in_graph = actual_node  # C
    print("actual node name in teh graph =", actual_node_name_in_graph, "\n")
    print("actual node name in complete tree =", actual_node_name_in_complete, "\n")
    actual_distance = complete_tree.nodes[actual_node_name_in_complete]['distance']
    next_adjacents = graph.adj[actual_node_name_in_graph]
    actual_node_parents = complete_tree.nodes[actual_node_name_in_complete]['parents']
    print("Actual node parents =", actual_node_parents)
    for node_name, node_details in next_adjacents.items():
        # same first letter means same node
        print('node name adjacent =', node_name)
        print('actual node parents =', actual_node_parents)
        # # I HAVE TO CORRECT THE CONDITION HERE ! ( ACTUAL_NODE_PARENTS IS A LOST , I HAVE TO CHECK FOR EVERY FIRST LETTER IN EVERY ITEM THERE )
        if not (isNodeAlreadyPassedBy(actual_node_parents, node_name)) and node_name[0] != actual_node[0]:
            child_name_in_complete = (node_name * level) + str(
                nodeNameCpt(complete_tree.nodes, (node_name * level)))  # C....C
            print("I will create a child node : ", child_name_in_complete)
            edge_weight = node_details['weight']
            actual_parents_child = list(actual_node_parents)
            actual_parents_child.append(actual_node)
            child_distance = actual_distance + edge_weight
            complete_tree.add_node(child_name_in_complete, distance=child_distance, parents=actual_parents_child)
            complete_tree.add_weighted_edges_from([(actual_node_name_in_complete, child_name_in_complete, edge_weight)])
            complete_tree_edges_lables[(actual_node_name_in_complete, child_name_in_complete)] = child_distance
            if level == len(graph.nodes)-1:
                path = actual_parents_child.copy()
                path.append(node_name)
                complete_tree_final_distances.append(
                    {"final_distance": child_distance + graph.edges[node_name, root_name]['weight'], "path": path})
                print("FINAL DISTANCES =", complete_tree_final_distances)
            complete_algorithm_recursive(graph, complete_tree, node_name[0], level + 1 , root_name)


def isNodeAlreadyPassedBy(parents: list[str], node_name: str):
    passed_by = False
    for parent in parents:
        if parent[0] == node_name[0]:
            passed_by = True
            break
    return passed_by


# if i want to create a CCC node and CCC1 , CCC2 already exists then i should name it CCC3
def nodeNameCpt(nodes, target_name):
    cpt = None
    for node in nodes:
        if (target_name in node):
            try:
                node_number = int(node.replace(target_name, "", 1))
                if cpt == None or node_number > cpt:
                    cpt = node_number
            except ValueError:
                useless = 2
    if cpt == None:
        cpt = 0
    else:
        cpt += 1
    return cpt
