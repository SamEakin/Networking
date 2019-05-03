# Networking Homework 5
#
#
import sys
import json
from collections import defaultdict

class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

def getInputArgs(): # py path.py [graph.json] [source] [destination]
        arg_count = len(sys.argv)
        print(arg_count)
        if arg_count < 4:
            print("Not enough arguments!")
            sys.exit(-1)
        else:
            file_name = sys.argv[1]
            source = sys.argv[2]
            destination = sys.argv[3]
            return file_name, source, destination


def dijsktra(graph, initial, end):
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path


####################

file_name, source, destination = getInputArgs()

network = Graph()
edges = []

with open(file_name) as json_file:
    data = json.load(json_file)
    for entry in data:
        print('src='+ entry['src'] + ' dst='+ entry['dst'] + ' w='+ entry['w'])
        edges.append((entry['src'], entry['dst'], int(entry['w'])))

for edge in edges: #deletes redudant duplicate edges
    src = edge[0]
    dst = edge[1]
    for otheredge in edges:
        if otheredge[1] == src:
            if otheredge[0] == dst:
                edges.remove(otheredge)

print(edges)
    
for edge in edges:
    network.add_edge(*edge)

path = dijsktra(network, source, destination)    
print(path)
