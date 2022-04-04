import random

from Community import join_new_community


# User class. Each person, after created an account, will have an object
# Class fields:
# neighbor: list of users
# t: time created an account
# name: just an id used for drawing the graph
# communities: List of communities this person has joined
# person_communities: List of Person-Community Edges
class Person:
    def __init__(self, t, name, is_directed):
        self.neighbors = []
        self.follower = []
        self.following = []
        self.t = t
        self.name = name
        self.cluster_coeff = []
        self.communities = []
        self.person_communities = []
        self.is_directed = is_directed

    # Removes a single node from the list of its neighbors
    def remove_neighbor(self, node, is_follower=True):
        if self.is_directed:
            if is_follower:
                if node in self.follower:
                    self.follower.remove(node)
                    node.remove_neighbor(self, is_follower=False)
                    return True
            else:
                if node in self.following:
                    self.following.remove(node)
                    node.remove_neighbor(self, is_follower=True)
                    return True
        else:
            if node in self.neighbors:
                self.neighbors.remove(node)
                node.remove_neighbor(self)
                return True
        return False

    # This method is used when a node deletes account. It removes itself from the set of neighbors of all its neighbors
    def remove_self(self):
        if self.is_directed:
            for neighbor in self.follower:
                neighbor.remove_neighbor(self, False)
            for neighbor in self.following:
                neighbor.remove_neighbor(self, True)
        else:
            for neighbor in self.neighbors:
                neighbor.remove_neighbor(self)
        for community in self.communities:
            community.remove_person(self)

    # Adds a neighbor. Returns False if node is already its neighbor
    def add_neighbor(self, node, is_follower=True):
        if self.is_directed:
            if is_follower:
                if node not in self.follower:
                    self.follower.append(node)
                    return True
            else:
                if node not in self.following:
                    self.following.append(node)
                    return True
            return False
        else:
            if node in self.neighbors:
                return False
            else:
                self.neighbors.append(node)
                return True

    def append_cluster_coeff(self, coeff):
        self.cluster_coeff.append(coeff)

    # Adds person_community to the list of edges and add the community to the list of communities
    # Returns False if person already exists in the community
    def join_community(self, person_community):
        community = person_community.community
        if community not in self.communities:
            self.communities.append(community)
            self.person_communities.append(person_community)
            return True
        else:
            return False

    # Removes community from the communities and removes the edge
    # Returns False if person is not in the community
    def leave_community(self, person_community):
        community = person_community.community
        if community not in self.communities:
            return False
        else:
            self.communities.remove(community)
            self.person_communities.remove(person_community)
            return True

    # This method chooses one of its communities randomly based on the entry time.
    # If this person is in no community, this method gets a random community and adds this person to that community
    def get_random_community(self, time):
        if len(self.communities) == 0:
            join_new_community(self, time)
            return self.communities[-1]
        else:
            times = [time / (time - pc.time + 1) for pc in self.person_communities]
            if time == 0:
                return self.person_communities[0].community
            random_pc = random.choices(self.person_communities, weights=times, k=1)
            return random_pc[0].community
