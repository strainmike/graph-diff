"""
This module generates a diff between two graphs.
"""
import pydot


def _add_all_sub_nodes(subgraph, nodes):
    for node in subgraph.get_nodes():
        nodes.add(node.get_name())
        print(node) # get_nodes makes new nodes every times its called, wtf
    for graph in subgraph.get_subgraphs():
        _add_all_sub_nodes(graph, nodes)


def add_diff_to_graph(initial, other, changed_nodes):
    """ Adds a diff to the initial graph passed in diffing it from the other graph
    """
    removed_nodes_names = set(initial.obj_dict["nodes"].keys()) - set(other.obj_dict["nodes"].keys())
    for removed_node_name in removed_nodes_names:
        removed_node = initial.get_node(removed_node_name)[0]
        removed_node.set_color("red")
        changed_nodes.add(removed_node.get_name())
    added_nodes_names = set(other.obj_dict["nodes"].keys()) - set(initial.obj_dict["nodes"].keys())
    for added_node_name in added_nodes_names:
        added_node = other.get_node(added_node_name)[0]
        added_node.set_color("green")
        initial.add_node(added_node)
        changed_nodes.add(added_node.get_name())

    removed_edges = set(initial.obj_dict["edges"].keys()) - set(other.obj_dict["edges"].keys())
    for removed_edge in removed_edges:
        edge = initial.get_edge(removed_edge)[0]
        edge.set_color("red")
        changed_nodes.add(edge.get_source())
        changed_nodes.add(edge.get_destination())

    added_edges = set(other.obj_dict["edges"].keys()) - set(initial.obj_dict["edges"].keys())
    for added_edge in added_edges:
        edge = other.get_edge(added_edge)[0]
        edge.set_color("green")
        initial.add_edge(edge)
        changed_nodes.add(edge.get_source())
        changed_nodes.add(edge.get_destination())

    same_subgraphs = set(initial.obj_dict["subgraphs"].keys()) & set(other.obj_dict["subgraphs"].keys())
    for subgraph in same_subgraphs:
        add_diff_to_graph(initial.get_subgraph(subgraph)[0], other.get_subgraph(subgraph)[0], changed_nodes)
    removed_subgraphs = set(initial.obj_dict["subgraphs"].keys()) - set(other.obj_dict["subgraphs"].keys())
    for removed_subgraph_name in removed_subgraphs:
        removed_subgraph = initial.get_subgraph(removed_subgraph_name)[0]
        removed_subgraph.set_bgcolor("red")
        changed_nodes.add(removed_subgraph.get_name())
        _add_all_sub_nodes(removed_subgraph, changed_nodes)
    added_subgraphs = set(other.obj_dict["subgraphs"].keys()) - set(initial.obj_dict["subgraphs"].keys())
    for added_subgraph_name in added_subgraphs:
        added_subgraph = other.get_subgraph(added_subgraph_name)[0]
        added_subgraph.set_bgcolor("green")
        initial.add_subgraph(added_subgraph)
        changed_nodes.add(added_subgraph.get_name())
        _add_all_sub_nodes(added_subgraph, changed_nodes)


def _get_edges_within_all_subgraphs(graph, connecting_node):
    for edge in graph.get_edges():
        if edge.get_source() == connecting_node or edge.get_destination() == connecting_node:
            yield edge
    for subgraph in graph.get_subgraphs():
        yield from _get_edges_within_all_subgraphs(subgraph, connecting_node)


def _find_node_by_name(graph, name):
    node = graph.get_node(name)
    if node:
        return node[0]
    for subgraph in graph.get_subgraphs():
        node = _find_node_by_name(subgraph, name)
        if node:
            return node
    return None


def _delete_node_and_connections(graph, node_name):
    graph.del_node(node_name)
    for edge in _get_edges_within_all_subgraphs(graph, node_name):
        graph.del_edge(edge.get_source(), edge.get_destination())
    for subgraph in graph.get_subgraphs():
        _delete_node_and_connections(subgraph, node_name)


def _visit_breadth_till_depth_and_add_to_set(graph, source_node, nodes_visited, depth, add_cluster=True):
    nodes_visited.add(source_node)
    if depth == 0:
        return
    nodes_to_visit = set()
    for edge in _get_edges_within_all_subgraphs(graph, source_node):
        print("in loop")
        nodes_to_visit.add(edge.get_source())
        nodes_to_visit.add(edge.get_destination())
    # if add_cluster:
        # node = _find_node_by_name(graph, source_node)
        # cluster = node.get_parent_graph()
        # if cluster.get_name() != graph.get_name():
            # for node in cluster.get_nodes():
                # nodes_to_visit.add(node)
            # for cluster in cluster.get_clusters():
                # nodes_to_visit.add(node)

    nodes_to_visit -= nodes_visited
    for node in nodes_to_visit:
        _visit_breadth_till_depth_and_add_to_set(graph, node, nodes_visited, depth - 1)


def _mark_nodes_at_distance_invisible(graph, changed_nodes, distance=5, add_cluster=True):
    invisible_nodes = set()
    _add_all_sub_nodes(graph, invisible_nodes)
    print(invisible_nodes)
    invisible_nodes -= changed_nodes
    print(invisible_nodes)
    print(changed_nodes)
    for node in changed_nodes:
        nodes_to_make_visisble = set()
        _visit_breadth_till_depth_and_add_to_set(graph, node, nodes_to_make_visisble, distance, add_cluster)
        print(nodes_to_make_visisble)
        invisible_nodes -= nodes_to_make_visisble
        if not invisible_nodes:
            break
    for node in invisible_nodes:
        # node_obj = _find_node_by_name(graph, node)
        _delete_node_and_connections(graph, node)
            # node_obj.set_style("invis")  # could maybe just kill the nodes?

    # TODO need to make their edges invis also....