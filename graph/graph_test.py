from graph.storage import GraphStorage

storage = GraphStorage()

# Create example nodes
node1 = {'id': 'order-service', 'type': 'Service', 'properties': {'port': 8082}}
node2 = {'id': 'payment-service', 'type': 'Service', 'properties': {'port': 8083}}

storage.upsert_node(node1)
storage.upsert_node(node2)

# Create edge
edge = {'source': 'order-service', 'target': 'payment-service', 'type': 'CALLS', 'properties': {'method': 'HTTP'}}
storage.upsert_edge(edge)

storage.close()
print("Nodes and edges inserted successfully!")
