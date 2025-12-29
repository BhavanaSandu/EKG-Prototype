import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class EKGProcessor:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def generate_cypher(self, user_query):
        system_context = """
        You are an expert Neo4j Database Engineer.
        The graph has nodes with types: 'service', 'team', 'infrastructure'.
        Relationships are: 'depends_on', 'owns'.

        Rules:
        1. Only return the Cypher query. No preamble.
        2. Use IDs like 'service:name' or 'team:name'.
        3. If you can't answer, return 'NOT_SUPPORTED'.

        Example:
        User: "Who owns payment-service?"
        Output: MATCH (t:team)-[:owns]->(s:service {name: 'payment-service'}) RETURN t.name
        """
        response = self.model.generate_content(f"{system_context}\n\nUser Question: {user_query}")
        return response.text.strip()