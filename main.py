# 400109638
# I used this source https://github.com/lingxuez/bayes-net/tree/master
import copy


class Node(object):
    def __init__(self, name=None):
        self.name = name
        self.parents = dict()
        self.children = dict()

    def add_parent(self, parent):
        pname = parent.name
        self.parents[pname] = parent

    def add_child(self, child):
        cname = child.name
        self.children[cname] = child


class BayesianNetwork(object):
    def __init__(self):
        # key = node's name,
        # value = Node object
        self.nodes = dict()

    def add_edge(self, edge):
        (parent_name, child_name) = edge

        if parent_name not in self.nodes:
            self.nodes[parent_name] = Node(name=parent_name)
        if child_name not in self.nodes:
            self.nodes[child_name] = Node(name=child_name)

        parent = self.nodes.get(parent_name)
        child = self.nodes.get(child_name)
        parent.add_child(child)
        child.add_parent(parent)

    def is_independent(self, n1, n2, observed):
        # ABOUT THIS METHOD:
        # we will observe all the paths from n1 to n2
        # if there is path from n1 to n2, then these two nodes are not independent!
        # detailed infos are below!

        # find the observed neighbors
        visited = copy.copy(observed)
        op = []
        while len(visited) > 0:
            next_node = self.nodes[visited.pop()]
            for parent in next_node.parents:
                op.append(parent)

        connected_nodes = [(n1, "up")]

        # save the array of visited nodes to avoid observing the repetitive paths!
        # (or just set a flag for visited nodes)
        visited = []

        while len(connected_nodes) > 0:
            node_num, path = connected_nodes.pop()
            pair = (node_num, path)
            node = self.nodes[node_num]

            # if the pair (node and path) is visited, don't do anything, if not, append it to visited array and go on!
            if pair not in visited:
                visited.append(pair)

                # found an active path from n1 to n2, so these two are not independent
                if node_num not in observed and node_num == n2:
                    return False

                # Handle the v-structure model with "up" and "down" paths
                # I have written the details about paths and their status at first

                if node_num not in observed and path == "up":
                    for parent in node.parents:
                        connected_nodes.append((parent, "up"))
                    for child in node.children:
                        connected_nodes.append((child, "down"))
                elif path == "down":
                    # active path
                    if node_num not in observed:
                        for child in node.children:
                            connected_nodes.append((child, "down"))
                    # v-structure
                    if node_num in observed or node_num in op:
                        for parent in node.parents:
                            connected_nodes.append((parent, "up"))
        return True

# ------------------------------------------------------------------------------------------
# NOTE #                                                                                   -
# first I'll say the active and inactive paths structure:                                  -
#                                                                                          -
# ********* ACTIVE PATH *********                                                          -
# u -> v -> z  ,  u -> v(observed) <- z  ,  u <- v -> z  ,  u -> (v -> x(observed)) <- z   -
#                                                                                          -
# ********* INACTIVE PATH *********                                                        -
# u -> v(observed) -> z  ,  u -> v <- z  ,  u <- v(observed) -> z                          -
# ------------------------------------------------------------------------------------------


bn = BayesianNetwork()
# number of nodes
n = int(input())
# number of edges
m = int(input())

for i in range(m):
    # input the parent (u) and child (v) nodes
    u, v = map(int, input().split("->"))
    bn.add_edge((u, v))

# number of tests
T = int(input())
for i in range(T):
    # nodes
    n1 = int(input())
    n2 = int(input())
    # input the observed nodes (visited)
    observed_nodes = list(map(int, input().split()))

    print(bn.is_independent(n1, n2, observed_nodes))