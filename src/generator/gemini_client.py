import time
from google import genai
from google.genai import types
from config.settings import GEMINI_API_KEY, GEMINI_MODEL_NAME

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = GEMINI_MODEL_NAME

    def generate_content(self, prompt, is_json=False):
        """Generates content with retry logic and extended timeout."""
        max_retries = 5
        retry_delay = 10 # seconds
        
        for attempt in range(max_retries):
            try:
                config = {}
                if is_json:
                    config["response_mime_type"] = "application/json"
                
                # Extended timeout for heavy bulk generation
                config["http_options"] = types.HttpOptions(timeout=180000) 
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config)
                )
                
                if not response or not response.text:
                    print(f"Empty response (Attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    return None
                return response.text

            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {e}")
                if "504" in str(e) or "503" in str(e) or "deadline" in str(e).lower():
                    if attempt < max_retries - 1:
                        print(f"Temporary error detected. Retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                        continue
                
                import traceback
                traceback.print_exc()
                return None
        return None

if __name__ == "__main__":
    # Simple test
    client = GeminiClient()
    result = client.generate_content("Hello, introduce yourself briefly.")
    if result:
        print("Success!")
    else:
        print("Failed.")
