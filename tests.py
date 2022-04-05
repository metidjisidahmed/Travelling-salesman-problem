import datetime
import os

from .main import *
from timeit import timeit

import pytest
import os

#to get the current working directory
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
directory = os.getcwd()

def testGreedy():
    print("DIRECTORY = \n",directory)
    time_before = datetime.datetime.now()
    graph = create_graph_from_excel_file(directory+'/data.xlsx')
    greedy_algorithm_init(graph, "A")
    time_after = datetime.datetime.now()
    print("Time Greedy algo =", (time_after - time_before).microseconds / 1000000, " Seconds ")

    return True


def testComplete():
    time_before = datetime.datetime.now()
    graph = create_graph_from_excel_file(directory+'/data.xlsx')
    result = complete_algorithm_init(graph, "A")
    time_after = datetime.datetime.now()
    print("Time Complete algo =", (time_after - time_before).microseconds / 1000000, " Seconds ")
    return True
