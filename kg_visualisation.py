from pyvis.network import Network
import pandas as pd

# Step 1: Read CSV file and extract data
import pickle
with open('EMBEDDINGS.pkl', 'rb') as f:
  df = pickle.load(f)

# Step 2: Select the first 30 rows and print head, relation, and tail
# for index, row in df.head(200).iterrows():
#     head = row['head']
#     relation = row['relation']
#     tail = row['tail']
    

# Step 3: Create a Pyvis network
net = Network()

# Add nodes and edges to the network
for index, row in df.head(3000).iterrows():
    try:
        head = row['head']
        relation = row['relation']
        tail = row['tail']
        
        net.add_node(head, label=head)
        net.add_node(tail, label=tail)
        net.add_edge(head, tail, label=relation)
    except:
        print(f"Row {index + 2}")

# Step 4: Generate HTML file without opening it in the browser
net.save_graph('knowledge_graph.html')

