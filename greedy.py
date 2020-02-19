import csv
#
# class Graph(object):
#     """ Graph data structure, undirected by default. """
#
#     def __init__(self, connections, directed=False):
#         self._graph = defaultdict(set)
#         self._directed = directed
#         self.add_connections(connections)
#
#     def add_connections(self, connections):
#         """ Add connections (list of tuple pairs) to graph """
#
#         for node1, node2 in connections:
#             self.add(node1, node2)
#
#     def add(self, node1, node2):
#         """ Add connection between node1 and node2 """
#
#         self._graph[node1].add(node2)
#         if not self._directed:
#             self._graph[node2].add(node1)
#
#     def remove(self, node):
#         """ Remove all references to node """
#
#         for n, cxns in self._graph.iteritems():
#             try:
#                 cxns.remove(node)
#             except KeyError:
#                 pass
#         try:
#             del self._graph[node]
#         except KeyError:
#             pass
#
#     def is_connected(self, node1, node2):
#         """ Is node1 directly connected to node2 """
#
#         return node1 in self._graph and node2 in self._graph[node1]
#
#     def find_path(self, node1, node2, path=[]):
#         """ Find any path between node1 and node2 (may not be shortest) """
#
#         path = path + [node1]
#         if node1 == node2:
#             return path
#         if node1 not in self._graph:
#             return None
#         for node in self._graph[node1]:
#             if node not in path:
#                 new_path = self.find_path(node, node2, path)
#                 if new_path:
#                     return new_path
#         return None
#
#     def __str__(self):
#         return '{}({})'.format(self.__class__.__name__, dict(self._graph))

# #Reading log file-------------------------------------------------------------------------------------
# with open('') as logfile:
#     readCSV = csv.reader(logfile, delimiter=',')


def get_graph(agents, observations):
    graph={}

    #Applying the sliding window over the observations------------------------------------------------------------------
    windows=get_windows(agents,observations)

    print("Applying the sliding window approach, we form the following windows: ")
    print(windows);print("\n")

    #Getting the list of candidate edges for each sliding window--------------------------------------------------------
    candidates=get_candidates(windows)

    print("Getting the list of candidate edges(i.e. possible edges in each window): ")
    print(candidates)
    num_candidates=((agents-1)*agents)/2
    print("There are "+str(agents)+" agents; hence we get "+str(num_candidates)+" candidate edges for each window.\n")

    #Implementing the greedy approach-----------------------------------------------------------------------------------
    for i in candidates:
         i.append(0)
    #If the list of candidates have a zero in the end, then it is unexplained.
    print("As done in step one, each list of candidate edges are marked unexplained with 0 in the end of each list: ")
    print(candidates);print("\n")

    return make_graph(greedy(candidates))

#Function to get windows------------------------------------------------------------------------------------------------
def get_windows(agents,observations):
    windows=[]
    runs = len(observations) - (agents - 1)
    start = 0;
    stop = agents
    for i in range(0, runs):
        temp_window = []
        for j in range(start, stop):
            temp_window.append(observations[j])
            # print(observations[j],end =" ")
        start += 1;
        stop += 1
        windows.append(temp_window)
    return windows

#Function to get candidate list-----------------------------------------------------------------------------------------
def get_candidates(windows):
    candidates=[]
    for candidate in windows:
        # print(candidate)
        edges=[]
        start = 0
        while start<len(candidate)-1:
            # print("start: "+str(start))
            for i in range(start, len(candidate)-1):
                # print(len(candidate)-1)
                temp=str(candidate[start])+str(candidate[i+1])
                # print(temp)
                edges.append(temp)
            start+=1
        # print(edges)
        candidates.append(edges)
    return candidates

#Function to execute the greedy approach--------------------------------------------------------------------------------
def greedy(candidates):
    E=[] #List of edges

    #Making a list of all candidate edges--------------------------
    all_candidates=get_all_candidates(candidates)

    #Counting the number of candidate edges and putting in dict----
    edges=get_edges(all_candidates)
    print("We now have a dictionary with all the edges and the number of occurrences: ")
    print(edges);print("\n")


    #Now, we execute step 2 and 3 in the greedy algorithm---------------------------------------------------------------------
    explained=1
    # print(edges)
    while explained<=len(candidates):
        big_edge="";edge_size=0
        for i in edges:
            if edges.get(i)>edge_size:
                big_edge=i
                edge_size=edges.get(i)
        print("\nIn the list of edges, the most occurring edge is: "+big_edge)
        E.append(big_edge)
        print("E is: "+str(E))
        print("Now, the candidate list will be marked as explained as follows:")
        edges.pop(big_edge)
        for candidate in candidates:
            if big_edge in candidate and candidate[-1]!=1:
                candidate[-1]=1
                explained+=1
                print(candidate)
    return E

def get_all_candidates(candidates):
    all_candidates=[]
    for i in candidates:
        for j in i:
            if j!=0:
                all_candidates.append(j)
    return all_candidates

def get_edges(all_candidates):
    edges = {}
    for edge in all_candidates:
        # print("Egde: "+edge)
        count = 1
        for j in range(all_candidates.index(edge) + 1, len(all_candidates)):
            reverse_edge = edge[::-1]
            if edge == all_candidates[j] or reverse_edge == all_candidates[j]:
                count += 1
            edges.update({str(edge): count})
    return edges

def make_graph(edges):
    #Code from Wiliam
    graph={}
    for i in range(0, len(edges)-1):
        if edges[i][0] not in graph:
            graph[edges[i][0]]=[edges[i][1]]
        elif edges[i][0] in graph:
            graph.get(edges[i][0]).append(edges[i][1])
        if edges[i][1] not in graph:
            graph[edges[i][1]]=[edges[i][0]]
        elif edges[i][1] in graph:
            graph.get(edges[i][1]).append(edges[i][0])
    return graph

O=["A","C","D","E","B","F","A","D"]
agentsAssumed=4
agentsTrue=3
print("\nStarting the graph generator...\n")
V=get_graph(agentsAssumed, O)
print("The edges generated by the greedy algorithm is as follows: ")
print(V)


















