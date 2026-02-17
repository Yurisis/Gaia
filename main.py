import argparse
import random
import os
import json
import time
from datetime import datetime
from src.generator.gemini_client import GeminiClient
from src.generator.prompts import Prompts
from src.publisher.html_generator import HtmlGenerator
from src.publisher.affiliate import AffiliateInjector
from config.settings import AMAZON_TAG, RAKUTEN_ID

def deploy_to_github():
    """Automates the git push process."""
    print("Deploying to GitHub...")
    try:
        os.system('git add .')
        os.system('git commit -m "Auto-deploy: New content generated"')
        os.system('git push origin main')
        print("Deploy successful.")
    except Exception as e:
        print(f"Deploy failed: {e}")

def process_article(topic, title, content, injector, generator):
    """Common logic to process a single article."""
    # 2. Inject Affiliate Links
    print(f"Injecting affiliate links for: {title}")
    
    # Generate structured product card HTML
    card_html = injector.generate_product_card(topic)
    
    # Ensure content is string and append card
    full_content = str(content) + "\n\n" + card_html
    full_content = injector.inject_links(full_content)

    # 3. Publish Content
    # Use microsecond for uniqueness in bulk mode
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"article_{timestamp}.html"
    
    filepath = generator.generate_article(title, full_content, filename)
    return filepath

def main():
    parser = argparse.ArgumentParser(description="Gaia Content Automation")
    parser.add_argument("--topic", type=str, help="Topic to write about")
    parser.add_argument("--type", type=str, default="article", choices=["article", "news"], help="Type of content")
    parser.add_argument("--bulk", type=int, default=0, help="Number of articles to generate in bulk")
    args = parser.parse_args()

    client = GeminiClient()
    injector = AffiliateInjector(amazon_tag=AMAZON_TAG, rakuten_id=RAKUTEN_ID)
    generator = HtmlGenerator()

    def clean_topic(text):
        """Removes leading numbers, bullets, and whitespace from topic."""
        # Remove leading bullets, numbers, dots, and whitespace
        # e.g. "1. Topic", "- Topic", "123. Topic"
        import re
        cleaned = re.sub(r'^[\d\.\-\*\s]+', '', text)
        return cleaned.strip()

    if args.bulk > 0:
        print(f"Starting Gaia Bulk Mode... Target: {args.bulk} articles")
        # Load topics
        topics_pool = []
        if os.path.exists("config/topics.txt"):
            with open("config/topics.txt", "r", encoding="utf-8") as f:
                topics_pool = [
                    clean_topic(line)
                    for line in f 
                    if line.strip() and len(line) < 50 and not line.strip().startswith("以下")
                ]
        
        if not topics_pool:
            print("No topics found in config/topics.txt for bulk generation.")
            return

        total_needed = args.bulk
        processed = 0
        batch_size = 3

        while processed < total_needed:
            current_batch_size = min(batch_size, total_needed - processed)
            # Pick unique topics if possible
            batch_topics = random.sample(topics_pool, current_batch_size)
            
            print(f"Generating batch of {current_batch_size} articles... ({processed}/{total_needed})")
            topics_str = ", ".join(batch_topics)
            print(f"Topics: {topics_str}")
            prompt = Prompts.BULK_ARTICLE.format(count=current_batch_size, topics=topics_str)
            
            try:
                print("Requesting content from Gemini (with 180s timeout)...")
                response_text = client.generate_content(prompt, is_json=True) # Ensure JSON request
                if not response_text:
                    print(f"Failed to generate batch for: {topics_str}. Skipping to next batch.")
                    processed += current_batch_size # Skip these as if processed to avoid infinite loop, or just skip
                    continue
                
                # Basic cleaning of response if it's wrapped in markdown code blocks
                clean_json = response_text.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:].strip()
                    if clean_json.endswith("```"):
                        clean_json = clean_json[:-3].strip()
                elif clean_json.startswith("```"):
                    clean_json = clean_json[3:].strip()
                    if clean_json.endswith("```"):
                        clean_json = clean_json[:-3].strip()
                
                try:
                    articles = json.loads(clean_json)
                except json.JSONDecodeError:
                    print("JSON Decode Error. Retrying raw response cleanup...")
                    # Sometimes Gemini returns extra text. Try to find [ ... ]
                    start = clean_json.find('[')
                    end = clean_json.rfind(']')
                    if start != -1 and end != -1:
                        clean_json = clean_json[start:end+1]
                        articles = json.loads(clean_json)
                    else:
                        raise

                for item in articles:
                    title = item.get('title', 'Untitled')
                    # Simple check if already exists to avoid duplicates
                    # (Implementation for checking file existence could be more robust)
                    process_article(item.get('topic', 'Unknown'), title, item.get('content', ''), injector, generator)
                    processed += 1
                
                # Update Index once per batch
                generator.update_index()
                print(f"Batch completed. Total processed: {processed}/{total_needed}")
                
            except Exception as e:
                print(f"Error in batch processing: {e}")
                if 'response_text' in locals() and response_text:
                    print(f"Raw response head (first 500 chars): {response_text[:500]}")
                print("Skipping this batch due to error.")
                processed += current_batch_size
                continue
            
            if processed < total_needed:
                print("Waiting 5 seconds before next batch...")
                time.sleep(5)
        
        # Final deploy
        deploy_to_github()

    else:
        # Determine Topic
        topic = "Daily Tech Trends" # Default
        if args.topic:
            topic = args.topic
        elif os.path.exists("config/topics.txt"):
            try:
                with open("config/topics.txt", "r", encoding="utf-8") as f:
                    lines = [
                        clean_topic(line)
                        for line in f 
                        if line.strip() and len(line) < 50 and not line.strip().startswith("以下")
                    ]
                if lines:
                    topic = random.choice(lines)
            except Exception as e:
                print(f"Error reading topics.txt: {e}")

        print(f"Starting Gaia... Topic: {topic}")

        # 1. Generate Content
        print("Generating content with Gemini...")
        
        # Select prompt based on type
        prompt_template = Prompts.AFFILIATE_ARTICLE if args.type == "article" else Prompts.NEWS_SUMMARY
        prompt = prompt_template.format(topic=topic)
        
        content = client.generate_content(prompt)

        if not content:
            print("Failed to generate content.")
            return

        # 2. Process and Save
        process_article(topic, topic, content, injector, generator)
        
        # Update Index
        generator.update_index()
        deploy_to_github()
        print("Done!")

if __name__ == "__main__":
    main()
