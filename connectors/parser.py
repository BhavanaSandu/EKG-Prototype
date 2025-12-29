import yaml
import os

class EKGConnector:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def parse_docker_compose(self):
        nodes = []
        edges = []
        path = os.path.join(self.data_dir, "docker-compose.yml")
        
        with open(path, 'r', encoding="utf-8") as f:
            data = yaml.safe_load(f)
            services = data.get('services', {})
            
            for name, config in services.items():
                node_id = f"service:{name}"
                # Create Node
                nodes.append({
                    "id": node_id,
                    "type": "service" if "build" in config else "infrastructure",
                    "name": name,
                    "properties": config.get('labels', {})
                })
                
                # Infer Dependency Edges
                for dep in config.get('depends_on', []):
                    edges.append({
                        "id": f"edge:{name}-depends_on-{dep}",
                        "type": "depends_on",
                        "source": node_id,
                        "target": f"service:{dep}"
                    })
        return nodes, edges

    def parse_teams(self):
        nodes = []
        edges = []
        path = os.path.join(self.data_dir, "teams.yaml")
        
        with open(path, 'r', encoding="utf-8") as f:
            data = yaml.safe_load(f)
            for team in data.get('teams', []):
                team_id = f"team:{team['name']}"
                nodes.append({
                    "id": team_id,
                    "type": "team",
                    "name": team['name'],
                    "properties": {"lead": team['lead']}
                })
                # Create Ownership Edges
                for service in team.get('owns', []):
                    edges.append({
                        "id": f"edge:{team['name']}-owns-{service}",
                        "type": "owns",
                        "source": team_id,
                        "target": f"service:{service}"
                    })
        return nodes, edges
if __name__ == "__main__":
    connector = EKGConnector()
    svc_nodes, svc_edges = connector.parse_docker_compose()
    team_nodes, team_edges = connector.parse_teams()

    print("Services:", svc_nodes)
    print("Edges:", svc_edges)
    print("Teams:", team_nodes)
    print("Ownership:", team_edges)