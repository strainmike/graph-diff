import graphdiff
import pydot
import os
from graphdiff.graphdiff import _mark_nodes_at_distance_invisible
this_dir = os.path.dirname(os.path.realpath(__file__))


# def test_diff():
    # before = pydot.graph_from_dot_file(os.path.join(this_dir,"before.gv"))[0]
    # after = pydot.graph_from_dot_file(os.path.join(this_dir,"after.gv"))[0]
    # changed_nodes = set()
    # graphdiff.add_diff_to_graph(before, after, changed_nodes)
    # print(before)

def test_diff_distance():
    before = pydot.graph_from_dot_file(os.path.join(this_dir,"before.gv"))[0]
    after = pydot.graph_from_dot_file(os.path.join(this_dir,"after.gv"))[0]
    changed_nodes = set()
    graphdiff.add_diff_to_graph(before, after, changed_nodes)
    _mark_nodes_at_distance_invisible(before, changed_nodes)
    # print(before)