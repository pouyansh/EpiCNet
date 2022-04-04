import random

# this is the set of all communities in the graph
from plot import plot_community_size_distribution

communities = []


# Each community of the graph will be an object
# Each object will have a list of people in that community
class Community:
    def __init__(self, person):
        self.people = [person]
        self.size = 1

    # Remove "person" from the community. If person is not in this community, returns False
    def remove_person(self, person):
        if person in self.people:
            self.people.remove(person)
            self.size -= 1
            if len(self.people) == 0:
                remove_from_communities(self)
            return True
        else:
            return False

    # Inserts "person" in the community. If person already exists in the community, returns False
    def add_person(self, person):
        if person in self.people:
            return False
        else:
            self.people.append(person)
            self.size += 1
            return True


# This class represent the edge connecting a person and a community
# It stores the person, the community, and the time the person entered the community
class PersonCommunity:
    def __init__(self, person, community, time):
        self.person = person
        self.community = community
        self.time = time


# This method adds person to a random community.
# If the randomly selected community already contained person, it does nothing.
# If person joins a community in this time step, return True. Otherwise, False
def join_new_community(person, time):
    if len(communities) == 0:
        community = Community(person)
        communities.append(community)
        add_person_to_community(person, community, time)
        return True
    else:
        community = random.choices(communities, weights=[c.size for c in communities], k=1)[0]
        if person in community.people:
            return False
        else:
            add_person_to_community(person, community, time)
            return True


# This method checks whether community is new. If so, it adds it to the set of communities
def add_to_communities(community):
    if community not in communities:
        communities.append(community)


# this method removes community from the list of communities
def remove_from_communities(community):
    if community in communities:
        communities.remove(community)


# Creates n communities, each with k people from users
def create_communities(n, k, users, time):
    for _ in range(n):
        picked_users = random.choices(users, k=k)
        community = Community(picked_users[0])
        communities.append(community)
        add_person_to_community(picked_users[0], community, time)
        for j in range(1, k):
            add_person_to_community(picked_users[j], community, time)


# Plots the distribution of community sizes
def plot_community_sizes(path):
    plot_community_size_distribution(communities, path)


# Adding person to community
def add_person_to_community(person, community, time):
    pc = PersonCommunity(person, community, time)
    person.join_community(pc)
    community.add_person(person)


# This method return the number of communities
def number_of_communities():
    return len(communities)


# This method return a list of community sizes
def community_sizes():
    return [len(community.people) for community in communities]


# This method clears the list of communities
def clear_communities():
    communities.clear()
