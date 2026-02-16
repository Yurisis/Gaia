import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL_NAME

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    def generate_content(self, prompt, is_json=False):
        """Generates content based on the given prompt."""
        try:
            if is_json:
                response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            else:
                response = self.model.generate_content(prompt)
            
            # Use candidate content to avoid blocked content issues simple check
            text = response.text
            print(f"Generated text length: {len(text)}")
            return text
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
