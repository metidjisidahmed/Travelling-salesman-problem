from .main import *

import pytest


def testImport():
    graph = create_graph_from_excel_file("C:\\Users\\pc\\Documents\\GitHub\\TPGO_TP_4\\data.xlsx")
    greedy_algorithm_init(graph, "A")
    return True
