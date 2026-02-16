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

def process_article(topic, title, content, injector, generator):
    """Common logic to process a single article."""
    # 2. Inject Affiliate Links
    print(f"Injecting affiliate links for: {title}")
    amz_link = injector.generate_search_link(topic, "amazon")
    rak_link = injector.generate_search_link(topic, "rakuten")
    
    links_md = f"\n\n## 価格をチェックする\n- [Amazonで見る]({amz_link})\n- [楽天で見る]({rak_link})"
    # Ensure content is string
    full_content = str(content) + links_md
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

    if args.bulk > 0:
        print(f"Starting Gaia Bulk Mode... Target: {args.bulk} articles")
        # Load topics
        topics_pool = []
        if os.path.exists("config/topics.txt"):
            with open("config/topics.txt", "r", encoding="utf-8") as f:
                topics_pool = [
                    line.strip().lstrip('-').lstrip('*').strip() 
                    for line in f 
                    if line.strip() and len(line) < 50 and not line.strip().startswith("以下")
                ]
        
        if not topics_pool:
            print("No topics found in config/topics.txt for bulk generation.")
            return

        total_needed = args.bulk
        processed = 0
        batch_size = 5

        while processed < total_needed:
            current_batch_size = min(batch_size, total_needed - processed)
            # Pick unique topics if possible
            batch_topics = random.sample(topics_pool, current_batch_size)
            
            print(f"Generating batch of {current_batch_size} articles... ({processed}/{total_needed})")
            topics_str = ", ".join(batch_topics)
            prompt = Prompts.BULK_ARTICLE.format(count=current_batch_size, topics=topics_str)
            
            response_text = client.generate_content(prompt, is_json=True)
            if not response_text:
                print("Failed to generate batch.")
                break
            
            try:
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
                
                articles = json.loads(clean_json)
                for item in articles:
                    process_article(item.get('topic', 'Unknown'), item.get('title', 'Untitled'), item.get('content', ''), injector, generator)
                    processed += 1
            except Exception as e:
                print(f"Error parsing bulk response: {e}")
                print(f"Raw response head: {response_text[:200]}")
                break
            
            # Update Index once per batch
            generator.update_index()
            print(f"Batch completed. Total processed: {processed}")
            
            if processed < total_needed:
                print("Waiting 5 seconds before next batch...")
                time.sleep(5)

    else:
        # Determine Topic
        topic = "Daily Tech Trends" # Default
        if args.topic:
            topic = args.topic
        elif os.path.exists("config/topics.txt"):
            try:
                with open("config/topics.txt", "r", encoding="utf-8") as f:
                    lines = [
                        line.strip().lstrip('-').lstrip('*').strip() 
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
        print("Done!")

if __name__ == "__main__":
    main()
