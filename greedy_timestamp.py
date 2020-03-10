import statistics

# #Reading log file-------------------------------------------------------------------------------------
# with open('') as logfile:
#     readCSV = csv.reader(logfile, delimiter=',')


def get_graph(agents, observations, times):
    graph={}

    #Applying the sliding window over the observations------------------------------------------------------------------
    windows=get_windows(agents,observations,times) #returns dictionary

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
        i.update(explained=0)
    #If the list of candidates have a 0 in the end, then it is unexplained.
    print("\nEach list of candidate edges are marked unexplained with 0 in the end of each dictionary: ")
    print(candidates);print("\n")
    return make_graph(greedy(candidates))

#Function to get windows------------------------------------------------------------------------------------------------
def get_windows(agents,observations,times):
    windows=[]
    runs = len(observations) - (agents - 1)
    start = 0;
    stop = agents
    for i in range(0, runs):
        temp_window = []
        temp_times = []
        for j in range(start, stop):
            temp_window.append(observations[j])
            temp_times.append(times[j])
        start += 1;
        stop += 1
        event_time = dict(zip(temp_window, temp_times))
        windows.append(event_time)
    return windows

#Function to get candidate list-----------------------------------------------------------------------------------------
def get_candidates(windows):
    candidates=[]
    for candidate in windows:
        # print(candidate)
        # print(windows)
        edges=[]
        time_means=[]
        start = 0
        candidate_keys=list(candidate.keys())
        candidate_values=list(candidate.values())
        # print(candidate_keys)
        while start<len(candidate)-1:
            # print("start: "+str(start))
            for i in range(start, len(candidate)-1):
                # print(len(candidate)-1)
                temp_edge=str(candidate_keys[start])+str(candidate_keys[i+1])
                temp_time=round(((candidate_values[start]+candidate_values[i+1])/2),4)
                # print(temp)
                time_means.append(temp_time)
                edges.append(temp_edge)
            # print(time_means)
            start+=1
        # print(edges)
        candidate_event_time = dict(zip(edges, time_means))
        candidates.append(candidate_event_time)
    return candidates

#Function to execute the greedy approach--------------------------------------------------------------------------------
def greedy(candidates):
    E=[] #List of edges
    T={}
    #Making a list of all candidate edges--------------------------
    all_candidates=get_all_candidates(candidates)
    #Counting the number of candidate edges and putting in dict----
    edges=get_edges(all_candidates)
    print("\nWe now have a dictionary with all the edges and the number of occurrences, probability, mean time, and variance: ")
    print(edges);print("\n")
    #Now, we execute step 2 and 3 in the greedy algorithm---------------------------------------------------------------------
    explained=1
    while explained<=len(candidates):
        big_edge="";edge_size=0
        for i in edges:
            if (edges.get(i))[1]>edge_size:
                big_edge=i
                edge_size=(edges.get(i))[1]
        print("\nIn the list of edges, the most occurring edge is: "+big_edge)
        E.append(big_edge)
        print("Edge list is now: "+str(E))
        # print("Now, the candidate list will be marked as explained as follows:")
        # T.update({edge:pop(big_edge)})
        T.update({big_edge:edges.pop(big_edge)})
        for candidate in candidates:
            # print(candidate)
            if big_edge in candidate and candidate.get("explained")!=1:
                candidate.update(explained=1)
                # candidate[-1]=1
                explained+=1
                # print(candidate)
    # print("edges")
    # print(edges)
    print("\nThe occurrance, time, variance, etc are:")
    print(T)
    return E

def get_all_candidates(candidates):
    all_candidates={}
    for i in candidates: #i is dict
        candidates_key=list(i.keys())
        candidates_values=list(i.values())
        for j in i: #j=key of dict
            if j!='explained':
                all_candidates.update({j:i.get(j)})
    # print("printing all candiates")
    # print(all_candidates)
    return all_candidates

def get_edges(all_candidates):
    edges = {}
    all_candidates_keys=list(all_candidates.keys())
    for edge in all_candidates_keys:
        count = 1
        X = []
        probability=0
        average_time = 0
        variance=0
        values=[]
        X.append(all_candidates.get(edge))
        # values=[count, probability, average_time, Variance]
        for j in range(all_candidates_keys.index(edge) + 1, len(all_candidates_keys)):
            reverse_edge = edge[::-1]
            if edge == all_candidates_keys[j] or reverse_edge == all_candidates_keys[j]:
                count += 1
                X.append(all_candidates.get(edge))
                if reverse_edge == all_candidates_keys[j]:
                    X.append(all_candidates.get(reverse_edge))
            edges.update({str(edge): count})
        probability = count/len(all_candidates)
        average_time=statistics.mean(X)
        if len(X)>1:
            variance=statistics.variance(X)
        else:
            variance=0
        values = [count,probability,average_time,variance]
        edges.update({str(edge): values})
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
O_dict={"A":2.3,"C":4.345,"D":6.234,"E":6.9,"B":7.536,"F":7.987,"A":9.213,"D":12.232}
O_times=[2.3,4.345,6.234,6.9,7.536,7.987,9.213,12.232]
agentsAssumed=4
agentsTrue=3
print("\nStarting the graph generator...\n")
Final_Graph=get_graph(agentsAssumed, O, O_times)
print("The edges generated by the greedy algorithm is as follows: ")
print(Final_Graph)

















