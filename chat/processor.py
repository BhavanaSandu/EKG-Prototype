import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

class EKGProcessor:
    def __init__(self):
        # Load API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=api_key)

        # Try to use a stable alias first, then fallback to experimental
        self.model_name = "models/gemini-flash-latest" 
        self.fallback_model = "models/gemini-2.0-flash-exp"

    def generate_cypher(self, user_query: str) -> str:
        system_context = """
You are an expert Neo4j Database Engineer.
The graph has nodes with types: service, team, infrastructure.
Relationships are: depends_on, owns.

Rules:
1. Only return the Cypher query. No explanation.
2. Use node properties like {name:'order-service'}.
3. If you cannot answer, return NOT_SUPPORTED.
"""
        import time
        
        def try_generate(model):
            # Simple retry logic for 429s
            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=f"{system_context}\n\nUser Question: {user_query}"
                    )
                    return response.text
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        time.sleep(2 ** attempt) # Exponential backoff: 1s, 2s, 4s
                        continue
                    raise e
            raise Exception("Rate limit exceeded after retries")

        try:
            try:
                generated_text = try_generate(self.model_name)
            except Exception as e:
                print(f"Primary model {self.model_name} failed: {e}")
                # Fallback
                generated_text = try_generate(self.fallback_model)
                
        except Exception as e:
            print(f"GenAI Error: {e}")
            return f"Error: {str(e)}"

        return generated_text.strip()
