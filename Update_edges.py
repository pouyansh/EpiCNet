import math
import random

from Community import join_new_community

p3 = 0.15  # the probability that each user gets added to a community
p4 = 0.1  # the probability that an edge of a node is deleted
n_e = 10  # expected value of the number of new edges to be added for active users
p6 = 0.25  # the probability that a person creates a new connection to a celebrity


# This method choose a random node from one of the random communities of this person and adds an edge to that node
def add_random_edge(user, time, graph, users, is_directed):
    if is_directed:
        # considering whether to add an edge to a celebrity or not
        p = p6
        x = random.random()
        if x < p and len(users) > 0:  # we should add an edge to a celebrity
            # celebrity = random.choice(celebrities)
            person = random.choices(users, weights=[len(person.follower) for person in users], k=1)[0]
            if person == user or person in user.following:
                return False
            user.add_neighbor(person, is_follower=False)
            if person.add_neighbor(user, is_follower=True):
                graph.add_edge(user.name, person.name)
                return True
            return False
    # Choosing a random community of user
    community = user.get_random_community(time)
    if len(community.people) == 1:
        return False

    # Choosing a person in the community other that self
    person = user
    while person == user:
        person = random.choice(community.people)

    if (is_directed and person in user.following) or (not is_directed and person in user.neighbors):
        return False
    else:
        user.add_neighbor(person, is_follower=False)
        # makes sure that before this step, self was not in the neighbors of person
        if person.add_neighbor(user, is_follower=True):
            graph.add_edge(user.name, person.name)
            return True
        return False


# This method determines (for each person) whether it is going to be added to a new community or it will have new edges
# Then, it will update the network based on the previous random decision
def add_connections_of_user(user, time, graph, users, is_directed):
    new_edges = 0
    p = p3
    x = random.random()
    if x < p:  # we should add it to a new community
        join_new_community(user, time)

    e = math.floor(n_e)
    for _ in range(e):
        is_added = add_random_edge(user, time, graph, users, is_directed)
        if is_added:
            new_edges += 1
    return new_edges


# Delete at most 1 connection of user with probability p4. The connection to be deleted is
# the connection with a randomly chosen neighbor
def delete_connections_of_user(user, graph, is_directed):
    p = p4
    x = random.random()
    deleted_edge = 0
    if is_directed:
        if x < p and len(user.following):  # delete a connection of the user
            random_neighbor = random.choices(user.following)[0]
            if graph.has_edge(user.name, random_neighbor.name):
                user.remove_neighbor(random_neighbor, is_follower=False)
                random_neighbor.remove_neighbor(user, is_follower=True)
                graph.remove_edge(user.name, random_neighbor.name)
                deleted_edge += 1
    else:
        if x < p and len(user.neighbors):  # delete a connection of the user
            random_neighbor = random.choices(user.neighbors)[0]
            if graph.has_edge(user.name, random_neighbor.name):
                user.remove_neighbor(random_neighbor)
                random_neighbor.remove_neighbor(user)
                graph.remove_edge(user.name, random_neighbor.name)
                deleted_edge += 1
    return deleted_edge


# This method updates the connections of each user
def update_connections(users, time, graph, is_directed):
    total_new_edges = 0
    total_deleted_edges = 0
    for user in users:
        total_new_edges += add_connections_of_user(user, time, graph, users, is_directed)
        total_deleted_edges += delete_connections_of_user(user, graph, is_directed)
    return total_new_edges, total_deleted_edges


# This method returns the parameters related to edge update
def get_params():
    return n_e, p4, p3, p6


# This method sets the parameters related to edge update
def set_params(e_new=n_e, p4_new=p4, p3_new=p3, p6_new=p6):
    global n_e, p4, p3, p6
    n_e = e_new
    p4 = p4_new
    p3 = p3_new
    p6 = p6_new
