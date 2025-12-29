from neo4j import GraphDatabase
import time

class GraphStorage:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password", retries=5, delay=3):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None

        # Retry logic for startup
        for attempt in range(retries):
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                # Test connection
                with self.driver.session() as session:
                    session.run("RETURN 1")
                print("Connected to Neo4j")
                break
            except Exception as e:
                print(f"Connection attempt {attempt+1} failed: {e}")
                time.sleep(delay)
        if not self.driver:
            raise Exception("Failed to connect to Neo4j after retries")

    def close(self):
        if self.driver:
            self.driver.close()

    def upsert_node(self, node_data: dict):
        """
        node_data example: {"label": "Person", "id": "123", "name": "Alice"}
        """
        label = node_data.pop("label")
        node_id = node_data.pop("id")

        with self.driver.session() as session:
            session.run(
                f"""
                MERGE (n:{label} {{id: $id}})
                SET n += $props
                """,
                id=node_id,
                props=node_data
            )

    def upsert_edge(self, edge_data: dict):
        """
        edge_data example: {
            "from": {"label": "Person", "id": "123"},
            "to": {"label": "Company", "id": "456"},
            "type": "OWNS"
        }
        """
        from_label = edge_data["from"]["label"]
        from_id = edge_data["from"]["id"]
        to_label = edge_data["to"]["label"]
        to_id = edge_data["to"]["id"]
        rel_type = edge_data["type"]

        with self.driver.session() as session:
            session.run(
                f"""
                MATCH (a:{from_label} {{id: $from_id}})
                MATCH (b:{to_label} {{id: $to_id}})
                MERGE (a)-[r:{rel_type}]->(b)
                """,
                from_id=from_id,
                to_id=to_id
            )