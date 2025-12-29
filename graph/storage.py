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
        label = node_data.pop("label", "Node")   # default label if missing
        node_id = node_data.pop("id")

        # Flatten nested "properties" dict into top-level props
        props = node_data.pop("properties", {})
        merged_props = {**node_data, **props}

        with self.driver.session() as session:
            session.run(
                f"""
                MERGE (n:{label} {{id: $id}})
                SET n += $props
                """,
                id=node_id,
                props=merged_props
            )

    def upsert_edge(self, edge_data: dict):
        """
        edge_data example:
        {
            "id": "edge:teamA-owns-serviceX",
            "type": "owns",
            "source": "team:teamA",
            "target": "service:serviceX"
        }
        """
        source_id = edge_data["source"]
        target_id = edge_data["target"]
        rel_type = edge_data["type"]

        with self.driver.session() as session:
            session.run(
                """
                MATCH (a {id: $source_id})
                MATCH (b {id: $target_id})
                MERGE (a)-[r:REL {type: $rel_type}]->(b)
                """,
                source_id=source_id,
                target_id=target_id,
                rel_type=rel_type
            )

    def upsert_graph(self, nodes: list, edges: list):
        """
        Wrapper to insert/update a whole graph.
        """
        for node in nodes:
            self.upsert_node(node)
        for edge in edges:
            self.upsert_edge(edge)