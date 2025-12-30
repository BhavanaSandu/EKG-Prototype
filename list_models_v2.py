
import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=api_key)
    with open("models.txt", "w") as f:
        for m in client.models.list():
            f.write(f"{m.name}\n")
    print("Models written to models.txt")
        
except Exception as e:
    print(f"Error: {e}")
