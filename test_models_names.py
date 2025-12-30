
import google.genai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

candidates = [
    "gemini-1.5-flash",
    "models/gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "models/gemini-1.5-flash-latest",
    "gemini-1.5-flash-001",
    "models/gemini-1.5-flash-001",
    "gemini-1.5-pro",
    "models/gemini-1.5-pro"
]

client = genai.Client(api_key=api_key)

print("Testing model names...")
for model_name in candidates:
    print(f"\n--- Testing {model_name} ---")
    try:
        response = client.models.generate_content(
            model=model_name, 
            contents="Hello"
        )
        print("SUCCESS")
        print(f"Response: {response.text}")
        break 
    except Exception as e:
        print(f"FAILED: {e}")
        time.sleep(1) # small delay
