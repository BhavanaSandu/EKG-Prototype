from graph.storage import GraphStorage

if __name__ == "__main__":
    db = GraphStorage()
    db.upsert_node({"label": "Person", "id": "1", "name": "Bhavana"})
    db.upsert_node({"label": "Company", "id": "2", "name": "Neo4j Inc."})
    db.upsert_edge({
        "from": {"label": "Person", "id": "1"},
        "to": {"label": "Company", "id": "2"},
        "type": "OWNS"
    })
    db.close()