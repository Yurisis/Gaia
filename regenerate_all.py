
import os
import json
import time
import random
from src.generator.gemini_client import GeminiClient
from src.generator.prompts import Prompts
from src.publisher.html_generator import HtmlGenerator
from src.publisher.affiliate import AffiliateInjector
from config.settings import AMAZON_TAG, RAKUTEN_ID

def regenerate_all_content():
    client = GeminiClient()
    html_gen = HtmlGenerator()
    affiliate = AffiliateInjector(amazon_tag=AMAZON_TAG, rakuten_id=RAKUTEN_ID)
    
    # 1. Get list of existing articles to regenerate
    # We want to keep the same topics.
    # We can parse the filename or title from existing HTML?
    # Or just read config/topics.txt and regenerate fresh? 
    # Reading topics.txt is cleaner and ensures we follow the "Bulk" logic.
    # However, user might have manually created some or we might lose the "date" in filename if we generate fresh.
    # The user said "Apply to all articles".
    # Let's read `config/topics.txt` and generate new articles for them.
    # We will archive old ones or just overwrite if filenames match (filenames refer to timestamp so they won't match).
    # Growing the blog is good.
    # But wait, "Apply improvements to all articles" usually means "Replace current content with better content".
    # If I generate new files with new timestamps, I'll double the article count (Old + New).
    # If I delete old ones, I lose history.
    # 
    # Better approach:
    # 1. Read `config/topics.txt`.
    # 2. For each topic, generate content.
    # 3. Save as new file.
    # 4. (Optional) Remove old files if they are "low quality".
    # 
    # Given the user wants to "Brush up", I should probably REPLACE the content of existing topics if possible, 
    # OR just generate a fresh batch and maybe cleaner to just move old `docs/*.html` to `docs/archive/`?
    # 
    # Let's generate NEW articles for all topics in `config/topics.txt`.
    # This ensures high quality from scratch.
    
    topics_file = "config/topics.txt"
    if not os.path.exists(topics_file):
        print("Topics file not found.")
        return

    with open(topics_file, "r", encoding="utf-8") as f:
        topics = [line.strip() for line in f if line.strip()]

    print(f"Found {len(topics)} topics. Starting regeneration...")
    
    # Batch processing
    batch_size = 2
    for i in range(0, len(topics), batch_size):
        batch_topics = topics[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} ({len(batch_topics)} topics)...")
        
        prompt = Prompts.BULK_ARTICLE.format(
            count=len(batch_topics),
            topics=", ".join(batch_topics)
        )
        
        try:
            response_text = client.generate_content(prompt)
            
            # Parse JSON
            try:
                # Clean JSON format
                json_text = response_text.strip()
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0].strip()
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0].strip()
                
                articles_data = json.loads(json_text)
                
                # Check if it's a list or single object
                if isinstance(articles_data, dict):
                    articles_data = [articles_data]
                
                for article in articles_data:
                    # Robust key access
                    title = article.get("title")
                    if not title:
                        title = "Untitled Article"
                        
                    content = article.get("content", "")
                    
                    # Ensure topic exists
                    topic = article.get("topic")
                    if not topic:
                        # Fallback: try to find topic in title or just use title
                        topic = title

                    # Inject Affiliate
                    # Simple injection for now
                    # We can use the affiliate injector to make a card
                    # But the content already has "Rating" and "Merit" boxes from prompt.
                    # We need to add the "Product Card" at the bottom.
                    
                    try:
                        product_card_html = affiliate.generate_product_card(topic)
                    except Exception as e:
                        print(f"    Affiliate Error for {topic}: {e}")
                        product_card_html = "" # Fail gracefully

                    
                    # Append product card to content
                    content += f"\n\n{product_card_html}"
                    
                    # Generate HTML
                    # Use a fixed timestamp or just current time? Current time is fine.
                    # Generate Filename
                    from datetime import datetime
                    filename = f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(100000, 999999)}.html"
                    html_gen.generate_article(title, content, filename)
                    print(f"  Generated: {title}")
                    
            except json.JSONDecodeError as e:
                print(f"  JSON Error in batch: {e}")
                print(f"  Raw output: {response_text[:100]}...")
                
        except Exception as e:
            print(f"  API Error: {e}")
            time.sleep(10)
            
        time.sleep(2) # Ease rate limits

    # Rebuild Index and Sitemap
    html_gen.update_index()
    html_gen.generate_sitemap()
    print("Regeneration complete. Index and Sitemap updated.")

if __name__ == "__main__":
    regenerate_all_content()
