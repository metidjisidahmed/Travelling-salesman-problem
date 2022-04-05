import datetime
import os

from .main import *
from timeit import timeit

import pytest

starting_node = "A"

def testGreedy():
    time_before = datetime.datetime.now()
    graph = create_graph_from_excel_file("C:\\Users\\pc\\Documents\\GitHub\\TPGO_TP_4\\data.xlsx")
    greedy_algorithm_init(graph, starting_node)
    time_after = datetime.datetime.now()
    print("Time Greedy algo =", (time_after - time_before).microseconds / 1000000, " Seconds ")

    return True


def testComplete():
    time_before = datetime.datetime.now()
    graph = create_graph_from_excel_file("C:\\Users\\pc\\Documents\\GitHub\\TPGO_TP_4\\data.xlsx")
    result = complete_algorithm_init(graph, starting_node)
    time_after = datetime.datetime.now()
    print("Time Complete algo =", (time_after - time_before).microseconds / 1000000, " Seconds ")
    return True
