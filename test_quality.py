
from src.generator.gemini_client import GeminiClient
from src.generator.prompts import Prompts
from src.publisher.html_generator import HtmlGenerator
from src.publisher.affiliate import AffiliateInjector
from config.settings import AMAZON_TAG, RAKUTEN_ID
import json
import os

def generate_test_article(topic):
    print(f"Generating test article for topic: {topic}")
    
    # Initialize components
    client = GeminiClient()
    html_gen = HtmlGenerator()
    affiliate = AffiliateInjector(amazon_tag=AMAZON_TAG, rakuten_id=RAKUTEN_ID)
    
    # 1. Generate Content
    prompt = Prompts.AFFILIATE_ARTICLE.format(topic=topic)
    markdown_content = client.generate_content(prompt)
    
    # 2. Extract Title (Simple extraction for test)
    lines = markdown_content.strip().split('\n')
    title = "Untitled"
    for line in lines:
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            break
        elif line.startswith("## "):  # sometimes AI messes up h1
             title = line.replace("## ", "").strip()
             break

    # If title is in the content as markdown, remove it from content to avoid double H1
    # specific logic might be needed depending on prompt output
    
    # 3. Add Affiliate Links
    # Note: Main.py usually handles this. Let's do a simplified version.
    # We need product names. For now, let's just insert the main topic link at the end.
    # Actually, let's use the affiliate injector properly if possible, 
    # but for a quick test, we perform basic injection.
    
    # The prompt output usually contains the article body.
    # Let's just generate the HTML.
    
    # 4. Generate HTML
    filename = "test_article_quality.html"
    html_gen.generate_article(title, markdown_content, filename)
    
    # 5. Inject Affiliate (Post-process)
    # Re-read file
    with open(os.path.join(html_gen.output_dir, filename), 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Inject simple search link for the topic
    # Using the same logic as main.py's simplistic approach for now
    if "product-card" not in html:
        # if AI didn't generate it (it likely won't unless prompt implies it perfectly)
        # Actually prompt DOES imply it now.
        pass
        
    print(f"Generated: {os.path.join(html_gen.output_dir, filename)}")

if __name__ == "__main__":
    generate_test_article("Anker Prime Power Bank (モバイルバッテリー)")
