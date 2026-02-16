from google import genai
from google.genai import types
from config.settings import GEMINI_API_KEY, GEMINI_MODEL_NAME

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = GEMINI_MODEL_NAME

    def generate_content(self, prompt, is_json=False):
        """Generates content based on the given prompt using the new google-genai SDK."""
        try:
            config = {}
            if is_json:
                config = {"response_mime_type": "application/json"}
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            
            print(f"Generated text length: {len(response.text)}")
            return response.text
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error generating content: {e}")
            return None

if __name__ == "__main__":
    # Simple test
    client = GeminiClient()
    result = client.generate_content("Hello, introduce yourself briefly.")
    if result:
        print("Success!")
    else:
        print("Failed.")
