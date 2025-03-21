from atlassian import Jira
import networkx as nx  # for visualisation of the tree
import matplotlib.pyplot as plt  # for visualisation of the tree

# use one of above objects depending on your instance type cloud or DC
jira_cloud = Jira(url="<url>", username="username", password="password")
jira_dc = Jira(url="url", token="<token>>")

"""

 Return list that contains the tree of the issue, with all subtasks and inward linked issues.
 be aware of following limitations:
 (!) Function only returns child issues from the same jira instance or from instance to which api key has access to.
 (!) User asssociated with API key must have access to the  all child issues in order to get them.
"""
"""
 Let's say we have a tree of issues:
 INTEGRTEST-2 is the root issue and it has 1 subtask from project TEST - TEST1
 and also two linked issues from project INTEGRTEST - INTEGRTEST-3 and INTEGRTEST-4.
 INTEGRTEST-4 has a subtask INTEGRTEST-6
 -------------- graph representation of the tree ----------------
INTEGRTEST-2
  TEST-1
  INTEGRTEST-3
  INTEGRTEST-4
    INTEGRTEST-6
 ----------------------------------------------------------------
"""
output = jira_cloud.get_issue_tree_recursive("INTEGRTEST-2")


# print(output) will return:
# [
# {'INTEGRTEST-2': 'TEST-1'},
# {'INTEGRTEST-2': 'INTEGRTEST-3'},
# {'INTEGRTEST-2': 'INTEGRTEST-4'},
# {'INTEGRTEST-4': 'INTEGRTEST-6'}
# ]
# now we can use this output to create a graph representation of the tree:
def print_tree(node, dict_list, level=0):
    children = [value for dict_item in dict_list for key, value in list(dict_item.items()) if key == node]
    print(("  " * level + node))
    for child in children:
        print_tree(child, dict_list, level + 1)


# or use this input to create a visualisation using networkx and matplotlib librarries or
# some js library like recharts or vis.js
def make_graph(dict_list):
    # Create a new directed graph
    G = nx.DiGraph()
    # Add an edge to the graph for each key-value pair in each dictionary
    for d in dict_list:
        for key, value in list(d.items()):
            G.add_edge(key, value)

    # Generate a layout for the nodes
    pos = nx.spring_layout(G)

    # Define a color map for the nodes
    color_map = []
    for node in G:
        if node.startswith("CYBER"):
            color_map.append("blue")
        else:
            color_map.append("red")

    # Draw the graph
    nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=1500)

    # Display the graph
    plt.show()
