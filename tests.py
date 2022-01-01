from .main import *

import pytest


def testGreedy():
    graph = create_graph_from_excel_file("C:\\Users\\pc\\Documents\\GitHub\\TPGO_TP_4\\data.xlsx")
    greedy_algorithm_init(graph, "A")
    return True


def testComplete():
    graph = create_graph_from_excel_file("C:\\Users\\pc\\Documents\\GitHub\\TPGO_TP_4\\data.xlsx")
    result =complete_algorithm_init(graph, "A")
    # print('---------- PARENTS FINAL -----------------------\n')
    # for node , node_details in result.nodes.items():
    #     print("Node = ", node,"\n")
    #     print("Parents =" , node_details,"\n")
    return True
