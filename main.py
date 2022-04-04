import os

from Community import number_of_communities, community_sizes, clear_communities, create_communities, \
    plot_community_sizes
from Person import Person
from plot import *
from utilities import *
from Update_edges import *
from compute_properties import *
import time

# Our graph
G = nx.Graph()

# Total people we consider in the problem
N = 10 ** 5

# These values are lists so that we can have all the data at each time
N_p = []  # Number of people not familiar with the network over time
N_d = []  # Number of deleted users over time
N_u = []  # Number of users over time
M = []  # Number of edges over time

# Probability parameters
p1 = 0.04  # U -> D
p2 = 0.04  # D -> U

# time
t_final = 100  # end time

# community size
initial_size = 100
beta = 0.15

# users
users = []

# clustering coefficient
global_clustering_coefficients = []

# diameter
diameters = []
connected_components = []
strong_components = []

# Variables to store the results of each run for multiple runs
final_n_p = []
final_n_d = []
final_n_u = []
final_m = []
final_clustering_coefficients = []
final_diameters = []
final_connected_components = []
final_degrees = []
final_person_community = []
final_community_sizes = []


def initialize_graph(is_directed):
    global G
    if is_directed:
        G = nx.DiGraph()
    N_p.append(N)
    N_d.append(0)
    N_u.append(1)
    M.append(0)
    # Creating the seed graph
    for i in range(1):
        G.add_node(i)
        users.append(Person(0, i, is_directed))


# This method generates a string consists of all parameters in the run
def generate_run_specs():
    n_e_param, p4_param, p3_param, p6_param = get_params()
    return "p1 = " + str(p1) + "\np2 = " + str(p2) + \
           "\nn_e = " + str(n_e_param) + "\np4 = " + str(p4_param) + "\np3 = " + str(p3_param) + \
           "\np6 = " + str(p6_param) + "\nN = " + str(N) + \
           "\ninitial_size = " + str(initial_size) + "\nbeta = " + str(beta)


def generate_run_results(is_directed):
    degree = "\ndegree = " + str([len(person.neighbors) for person in users])
    if is_directed:
        degree = "\nout-degree = " + str([len(person.following) for person in users]) + \
                 "\nin-degree = " + str([len(person.follower) for person in users])
    return "#users = " + str(len(users)) + \
           "\n#edges = " + str(M[-1]) + \
           "\n#commuities = " + str(number_of_communities()) + \
           "\n\nN_p = " + str(N_p) + "\nN_u = " + str(N_u) + "\nN_d = " + str(N_d) + "\nM = " + str(M) + \
           degree + \
           "\naverage degree = " + str([2 * M[q] / N_u[q] for q in range(len(N_u))]) + \
           "\ncommunity sizes = " + str(community_sizes()) + \
           "\nperson community = " + str([len(person.communities) for person in users])


# returns the probability p0 at time step 'time'
def calculate_p0(t):
    return math.exp((t - (2 * t_final / 3)) / (t_final / 8)) / math.pow(
        (1 + math.exp((t - (2 * t_final / 3)) / (t_final / 8))), 2) / 10


# Creates account for "count" many people at time "time"
def add_users(count, t, name, is_directed):
    new_users = []
    for _ in range(count):
        person = Person(t, name, is_directed)
        new_users.append(person)
        users.append(person)
        G.add_node(name)
        name += 1
    return name


# This method deletes objects and their edges
def delete_users(count, is_directed):
    deleted_edges_count = 0
    items_to_delete = random.sample(users, k=min(len(users), count))
    for item in items_to_delete:
        deleted_edges_count += len(item.neighbors)
        if is_directed:
            deleted_edges_count += len(item.follower) + len(item.following)
        item.remove_self()
        users.remove(item)
        G.remove_node(item.name)
    return deleted_edges_count


# updates the size of the compartments at time step 't'
def update_compartments(t, name, is_directed):
    p0 = calculate_p0(t)

    # Creating objects for new nodes
    p_to_u = calculate_binomial(p0, N_p[-1])
    d_to_u = calculate_binomial(p2, N_d[-1])
    name = add_users(p_to_u + d_to_u, t, name, is_directed)

    # Deleting objects from active and inactive users
    deleted_edges_count = 0
    u_to_d = calculate_binomial(p1, N_u[-1])
    deleted_edges_count += delete_users(u_to_d, is_directed)

    # Updating compartments sizes
    n_p = N_p[-1] - p_to_u
    n_u = N_u[-1] + p_to_u + d_to_u - u_to_d
    n_d = N_d[-1] - d_to_u + u_to_d
    N_p.append(n_p)
    N_d.append(n_d)
    N_u.append(n_u)
    return name, deleted_edges_count, p_to_u + d_to_u - u_to_d


# This method clears all lists and graphs after each run
def clear():
    N_p.clear()
    N_d.clear()
    N_u.clear()
    M.clear()
    global_clustering_coefficients.clear()
    diameters.clear()
    connected_components.clear()
    users.clear()
    G.clear()
    clear_communities()


# This method plots all the results gathered from multiple runs
def plot_multiple_runs(path, changing_param):
    plot_time_based(values=final_m, title="",
                    y_label="Number of edges", legends=changing_param, path=path, name="edges")
    plot_time_based(values=final_n_u, title="",
                    y_label="Number of users", legends=changing_param, path=path, name="users")
    plot_distribution(values=final_degrees, title="",
                      x_label="Degree", y_label="Users", legends=changing_param, path=path, name="degree")
    plot_time_based(values=final_diameters, title="",
                    y_label="Diameter", legends=changing_param, path=path, name="diameter")
    plot_time_based(values=final_clustering_coefficients, title="",
                    y_label="Clustering Coefficient", legends=changing_param, path=path, name="clustering_coefficient")
    plot_distribution(values=final_person_community, title="",
                      x_label="Community per person", y_label="Users", legends=changing_param, path=path,
                      name="person-community")
    plot_distribution(values=final_community_sizes, title="",
                      x_label="Size of Community", y_label="Communities", legends=changing_param, path=path,
                      name="community-size")
    plot_time_based(
        values=[[2 * final_m[j][k] / final_n_u[j][k] for k in range(len(final_m[j]))] for j in range(len(final_m))],
        title="",
        y_label="Average degree", legends=changing_param, path=path, name="average-degree")


# This method plots the results of one run
def plotting(parent_path, is_directed):
    # Creating a folder to store the plots, specs, and result
    with open(parent_path + "/run_id.txt", 'r') as f:
        contents = int(f.readlines()[0])
    with open(parent_path + "/run_id.txt", 'w') as f:
        f.write(str(contents + 1))
    path = os.path.join(parent_path + "/", "run_" + str(contents))
    os.mkdir(path)

    # Storing parameters and results
    with open(path + "/run_specs.txt", 'a') as f:
        f.write(generate_run_specs())

    with open(path + "/results.txt", 'a') as f:
        f.write(generate_run_results(is_directed))

    # Plotting
    plot_edges(M, path)
    plot_users(N_u, path)
    plot_degree_distribution(users, path, is_directed)
    if is_directed:
        plot_components(connected_components, strong_components, path)
    else:
        plot_global_diameter(diameters, connected_components, path)
    plot_global_clustering_coefficient(global_clustering_coefficients, path)
    plot_person_community_degree_distribution(users, path)
    plot_community_sizes(path)
    plot_average_degree(N_u, M, path, is_directed)
    plot_compartments(N_p, N_u, N_d, path)

    # compute node wise clustering coefficient at each time step
    node_wise_cluster_coefficient_dict = compute_local_clustering_coefficient(G)
    plot_local_clustering_coefficient(list(node_wise_cluster_coefficient_dict.values()), path)
    return path


# This method runs the program
def run(is_directed=False, path="plots"):
    initialize_graph(is_directed)
    name_counter = len(users)
    # This for loop goes over each time step and updates the network at each time
    for j in range(t_final):
        print(j)
        name_counter, deleted_edges_count, new_users_count = update_compartments(j + 1, name_counter, is_directed)
        M.append(M[-1] - deleted_edges_count)

        # Creating new communities for this time step
        if new_users_count > 0:
            create_communities(math.floor(beta * new_users_count),
                               min(initial_size, math.ceil(len(users) / 2)),
                               users, j)

        # Updating the edges
        new_edges_count, deleted_edges_count = update_connections(users, j, G, is_directed)
        M[-1] += new_edges_count - deleted_edges_count

        # Computing some graph properties
        if is_directed:
            connected_components.append(nx.number_weakly_connected_components(G))
            strong_components.append(nx.number_strongly_connected_components(G))

            global_clustering_coefficients.append(nx.algorithms.average_clustering(G))
        else:
            diameter, components, clustering = compute_properties(G, users)
            diameters.append(diameter)
            connected_components.append(components)
            global_clustering_coefficients.append(clustering)

    # Plotting the graph properties
    result_path = plotting(path, is_directed)

    # graph analysis on the final graph and write the result to a file
    compute_average_neighbor_degree(G, users, result_path)


# Running the program
start_time = time.time()
run(is_directed=False)
end_time = time.time()

print("--- %s seconds ---" % (end_time - start_time))
