import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-flash-latest")
AMAZON_TAG = os.getenv("AMAZON_TAG", "demo-22")
RAKUTEN_ID = os.getenv("RAKUTEN_ID", "demo-11")
GOOGLE_ANALYTICS_ID = os.getenv("GOOGLE_ANALYTICS_ID", "G-XXXXXXXXXX") # Placeholder

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
