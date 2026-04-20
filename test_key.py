import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".env"))

key = os.getenv("GOOGLE_API_KEY")
print("Key found:", key[:10] + "..." if key else "NOT FOUND")