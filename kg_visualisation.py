import csv
import json
import networkx as nx
from graphviz import Digraph

# Step 1: Read CSV file and parse JSON-formatted triplets
triplets = []
with open('triplets_for_all_dates.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        triplet = json.loads(row['triplets'])
        triplets.append(triplet)

# Select the first 30 triplets for testing purposes
triplets = triplets[:30]

# Step 2: Construct a directed graph using NetworkX
G = nx.DiGraph()

# Add edges to the graph
for triplet in triplets:
    head, relation, tail = triplet['head'], triplet['relation'], triplet['tail']
    G.add_edge(head, tail, label=relation)

# Step 3: Visualize the graph using Graphviz
graph = Digraph(format='png')
for node in G.nodes():
    graph.node(node)

for edge in G.edges(data=True):
    source, target, label = edge
    graph.edge(source, target, label=label['label'])

graph.render('knowledge_graph', view=True)
