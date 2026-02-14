import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL_NAME

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    def generate_content(self, prompt):
        """Generates content based on the given prompt."""
        try:
            response = self.model.generate_content(prompt)
            print(f"Response: {response.text}")
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
