#!/usr/bin/env python
"""
This module generates a diff between two graphs.
"""


def add_diff_to_graph(initial, other):
    """ Adds a diff to the initial graph passed in diffing it from the other graph
    """
    removed_nodes_names = set(initial.obj_dict["nodes"].keys()) - set(other.obj_dict["nodes"].keys())
    for removed_node_name in removed_nodes_names:
        initial.get_node(removed_node_name)[0].set_color("red")
    added_nodes_names = set(other.obj_dict["nodes"].keys()) - set(initial.obj_dict["nodes"].keys())
    for added_node_name in added_nodes_names:
        added_node = other.get_node(added_node_name)[0]
        added_node.set_color("green")
        initial.add_node(added_node)

    removed_edges = set(initial.obj_dict["edges"].keys()) - set(other.obj_dict["edges"].keys())
    for removed_edge in removed_edges:
        initial.get_edge(removed_edge)[0].set_color("red")
    added_edges = set(other.obj_dict["edges"].keys()) - set(initial.obj_dict["edges"].keys())
    for added_edge in added_edges:
        edge = other.get_edge(added_edge)[0]
        edge.set_color("green")
        initial.add_edge(edge)

    same_subgraphs = set(initial.obj_dict["subgraphs"].keys()) & set(other.obj_dict["subgraphs"].keys())
    for subgraph in same_subgraphs:
        add_diff_to_graph(initial.get_subgraph(subgraph)[0], other.get_subgraph(subgraph)[0])
    removed_subgraphs = set(initial.obj_dict["subgraphs"].keys()) - set(other.obj_dict["subgraphs"].keys())
    for removed_subgraph in removed_subgraphs:
        initial.get_subgraph(removed_subgraph)[0].set_bgcolor("red")
    added_subgraphs = set(other.obj_dict["subgraphs"].keys()) - set(initial.obj_dict["subgraphs"].keys())
    for added_subgraph in added_subgraphs:
        other_subgraph = other.get_subgraph(added_subgraph)[0]
        other_subgraph.set_bgcolor("green")
        initial.add_subgraph(other_subgraph)
