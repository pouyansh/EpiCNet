import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import matplotlib.patches as mpatches

# These are the colors used to plot multiple diagrams
colors = ["dimgrey", "orange", "green", "cornflowerblue", "red", "darkviolet"]


# This is a method that is used to plot time-based data
def plot_time_based(values, title, y_label, legends, path, name, color=(0, 0, 0), mult=1):
    handles = []
    for i in range(len(values)):
        if color == (0, 0, 0):
            new_color = colors[i]
        else:
            new_color = color
        handles.append(mpatches.Patch(color=new_color, label=legends[i]))
        plt.plot([j * mult for j in range(len(values[i]))], values[i], '-', color=new_color)
    plt.title(title)
    plt.xlabel('time')
    plt.ylabel(y_label)
    if len(values) > 1:
        plt.legend(handles=handles)

    plt.savefig(path + "/" + name + ".png")
    plt.clf()


# Plotting the distribution
def plot_distribution(values, title, x_label, y_label, legends, path, name, log=False, color=(0, 0, 0), kde=False):
    max_val = 0
    handles = []
    for i in range(len(values)):
        if color == (0, 0, 0):
            new_color = colors[i]
        else:
            new_color = color
        handles.append(mpatches.Patch(color=new_color, label=legends[i]))
        sns.distplot(values[i], kde=kde, color=new_color, hist=not kde)
        max_val = max([max_val, max(values[i])])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(0, max_val)
    if len(values) > 1:
        plt.legend(handles=handles)
    if log:
        plt.xscale('log')

    plt.savefig(path + "/" + name + ".png")
    plt.clf()


# Plotting number of edges
def plot_edges(m, path):
    plot_time_based(values=[m], title="Number of edges",
                    y_label="Number of edges", legends=["NA"], path=path, name="edges")


# Plotting number of users
def plot_users(n_u, path):
    plot_time_based(values=[n_u], title="Number of users",
                    y_label="Number of users", legends=["NA"], path=path, name="users")


# Plotting the average degree
def plot_average_degree(n_u, m, path, is_directed):
    if is_directed:
        avg_deg = [[m[i] / n_u[i] for i in range(len(n_u))]]
        plot_time_based(values=avg_deg, title="Average degree",
                        y_label="Average following/follower", legends=["NA"], path=path, name="average-degree")
    else:
        avg_deg = [[2 * m[i] / n_u[i] for i in range(len(n_u))]]
        plot_time_based(values=avg_deg, title="Average degree",
                        y_label="Average degree", legends=["NA"], path=path, name="average-degree")


# Plotting the size of the compartments over time
def plot_compartments(n_p, n_u, n_d, path):
    plot_time_based(values=[n_p, n_u, n_d], title="Size of the compartments",
                    y_label="Size", legends=["Unassociated", "Registered", "Deleted"], path=path, name="compartments")


# Plotting the degree distribution
def plot_degree_distribution(users, path, is_directed):
    if is_directed:
        out_degree = [len(user.following) for user in users]
        in_degree = [len(user.follower) for user in users]
        plot_distribution(values=[out_degree, in_degree], title="Degree distribution",
                          x_label="Degree", y_label="Users",
                          legends=["followings", "followers"],
                          path=path, name="degree")
        plot_distribution(values=[out_degree, in_degree], title="Degree distribution",
                          x_label="Degree", y_label="Users",
                          legends=["followings", "followers"],
                          path=path, name="degree-kde", kde=True)
    else:
        degree = [[len(user.neighbors) for user in users]]
        plot_distribution(values=degree, title="Degree distribution",
                          x_label="Degree", y_label="Users", legends=["NA"], path=path, name="degree")


# plotting clustering coefficient of the whole graph i.e. global clustering coefficient across all time steps
def plot_global_clustering_coefficient(clustering_coefficients, path):
    plot_time_based(values=[clustering_coefficients], title="Clustering Coefficient",
                    y_label="Clustering Coefficient", legends=["NA"], path=path, name="clustering_coefficient",
                    mult=3)


# plotting diameter of the whole graph
def plot_global_diameter(diameters, connected_components, path):
    plot_time_based(values=[diameters, connected_components], title="Diameter and connected components",
                    y_label="Value", legends=["Diameter", "Connected Components"], path=path, name="diameter")


# plot clustering coefficient of each node in a certain time step
def plot_local_clustering_coefficient(clustering_coefficients, path):
    plot_distribution(values=[clustering_coefficients], title="Node-wise clustering coefficient",
                      x_label="Clustering Coefficient", y_label="Users", legends=["NA"], path=path, name="local_cc")


# Plotting the person-community degree distribution
def plot_person_community_degree_distribution(users, path):
    degree = [[len(user.communities) for user in users]]
    plot_distribution(values=degree, title="Communities per person", x_label="Community per person", y_label="Users",
                      legends=["NA"], path=path, name="person-community")


# Plotting the distribution of size of the communities
def plot_community_size_distribution(communities, path):
    sizes = [[len(community.people) for community in communities]]
    plot_distribution(values=sizes, title="Size of communities", x_label="Size of Community", y_label="Communities",
                      legends=["NA"], path=path, name="community-size")


# plotting the number of components
def plot_components(weak_components, strong_components, path):
    plot_time_based(values=[weak_components], title="Number of Weak connected components",
                    y_label="Weak connected components", legends=["NA"], path=path, name="weak_components")
    plot_time_based(values=[strong_components], title="Number of Strongly connected components",
                    y_label="Strongly connected components", legends=["NA"], path=path, name="strong_components")


# Plotting the graph
def plot_graph(g):
    options = {
        'node_color': 'blue',
        'node_size': 10,
        'width': 1,
    }
    nx.draw_random(g, **options)
    plt.show()


# Plots the data in a log-log scale
def plot_log_log(values, title, x_label, y_label, legends):
    handles = []
    for i in range(len(values)):
        new_color = colors[i]
        handles.append(mpatches.Patch(color=new_color, label=legends[i]))
        sns.distplot(values[i], kde=True, color=new_color, hist=False)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xscale('log')
    plt.yscale('log')

    plt.savefig("Plots/runs/log-log.png")
    plt.clf()
