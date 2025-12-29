import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

class EKGProcessor:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        # Use a model you VERIFIED exists
        self.model_name = "models/gemini-pro-latest"

    def generate_cypher(self, user_query: str) -> str:
        system_context = """
You are an expert Neo4j Database Engineer.
The graph has nodes with types: service, team, infrastructure.
Relationships are: depends_on, owns.

Rules:
1. Only return the Cypher query. No explanation.
2. Use node properties like {name: 'order-service'}.
3. If you cannot answer, return NOT_SUPPORTED.

Example:
MATCH (t:team)-[:owns]->(s:service {name:'payment-service'})
RETURN t.name
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"{system_context}\n\nUser Question: {user_query}"
        )

        return response.text.strip()
