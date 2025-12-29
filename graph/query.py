from neo4j import GraphDatabase

class QueryEngine:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_owner(self, node_id):
        """
        Finds the team node connected to a service.
        """
        query = """
        MATCH (t:team)-[:owns]->(s:service {id: $id})
        RETURN t
        """
        with self.driver.session() as session:
            result = session.run(query, id=node_id)
            return [record["t"] for record in result]

    def blast_radius(self, node_id):
        """
        Finds all nodes connected to a service up to 5 levels deep.
        """
        upstream = """
        MATCH (n {id: $id})<-[:DEPENDS_ON*1..5]-(dependent)
        RETURN dependent
        """
        downstream = """
        MATCH (n {id: $id})-[:DEPENDS_ON*1..5]->(dependency)
        RETURN dependency
        """
        with self.driver.session() as session:
            up = session.run(upstream, id=node_id)
            down = session.run(downstream, id=node_id)
            return {
                "upstream": [record["dependent"] for record in up],
                "downstream": [record["dependency"] for record in down]
            }

    def find_path(self, start_id, end_id):
        """
        Uses shortestPath to find how two services connect.
        """
        query = """
        MATCH (a {id: $start}), (b {id: $end}),
        p = shortestPath((a)-[:DEPENDS_ON*]-(b))
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query, start=start_id, end=end_id)
            return [record["p"] for record in result]