import networkx as nx
import random
from plot import plot_distribution


# This method computes number of connected components, diameter, and clustering coefficient of the graph
def compute_properties(graph, users):
    diameter = 0
    # compute the number of components
    components = [len(c) / len(users) for c in sorted(nx.connected_components(graph), key=len, reverse=True)]
    # If the graph is connected, then we compute an upperbound on the diameter of the graph as well
    if len(components) == 1:
        random_user = random.choice(users).name
        diameter = 2 * nx.algorithms.distance_measures.eccentricity(graph, random_user)

    return diameter, len(components), nx.algorithms.average_clustering(graph)


# This method computes the clustering coefficient for each user
def compute_local_clustering_coefficient(graph):
    node_wise_cluster_coefficient_dict = nx.algorithms.clustering(graph)
    return node_wise_cluster_coefficient_dict


# Compute node connectivity of final graph and write result to a file
def compute_node_connectivity(graph, path):
    print("START: compute node connectivity")
    connectivity = nx.node_connectivity(graph)
    with open(path + "/graph_params.txt", "a") as f:
        f.write("node connectivity = " + str(connectivity))
    print("END: compute node connectivity")


# Compute independent set size of final graph and write to a file
def compute_independent_set(graph, path):
    print("START: compute independent set")
    independent_set_size = len(nx.algorithms.approximation.clique.maximum_independent_set(graph))
    with open(path + "/graph_params.txt", "a") as f:
        f.write("independent set = " + str(independent_set_size))
    print("END: compute independent set")


# Compute dominating set size of final graph and write to a file
def compute_dominating_set(graph, path):
    print("START: compute dominating set")
    graph_params_file_path = path + "/graph_params.txt"
    print("Writing dominating set to " + graph_params_file_path)
    dominating_set_size = len(nx.algorithms.dominating.dominating_set(graph))
    with open(path + "/graph_params.txt", "a") as f:
        f.write("dominating set = " + str(dominating_set_size))
    print("END: compute dominating set")


# compute and plot distribution of clique sizes in final graph
def compute_clique(graph, path):
    print("START: compute clique")
    maximal_cliques = list(nx.find_cliques(graph))
    clique_sizes = [len(c) for c in maximal_cliques]
    plot_distribution(values=[clique_sizes], title="",
                      x_label="Size of the maximal clique", y_label="Frequency", legends=[""], path=path,
                      name="clique_size")
    print("END: compute clique")


# compute and plot distribution of average neighbor degree in final graph
def compute_average_neighbor_degree(graph, users, path):
    print("START: compute average neighbour degree")
    avg_neighbor_degree = nx.average_neighbor_degree(graph)
    average_neighbor_degree = list(avg_neighbor_degree.values())
    degrees = [len(person.neighbors) for person in users]
    plot_distribution(values=[average_neighbor_degree, degrees], title="",
                      x_label="Degree", y_label="Frequency", legends=["Neighbor's degree", "Node's degree"], path=path,
                      name="Neighbor_degree")
    dif = []
    for person in users:
        dif.append(avg_neighbor_degree.get(person.name) - len(person.neighbors))
    plot_distribution(values=[dif], title="",
                      x_label="Neighbor's degree - Node's degree", y_label="Frequency",
                      legends=[""], path=path,
                      name="Neighbor_Node_degree")
    positive = 0
    negative = 0
    for d in dif:
        if d > 0:
            positive += 1
        if d < 0:
            negative += 1
    with open(path + "/graph_params.txt", "a") as f:
        f.write("\nAverage Neighbor Degree > Node degree = " + str(positive))
        f.write("\nAverage Neighbor Degree < Node degree = " + str(negative))
    print("END: compute average neighbor degree")
