import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=Path(".env"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List all available models that support embedding
for model in genai.list_models():
    if "embed" in model.name.lower():
        print(model.name)