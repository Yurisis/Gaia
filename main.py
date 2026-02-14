import argparse
from datetime import datetime
from src.generator.gemini_client import GeminiClient
from src.generator.prompts import Prompts
from src.publisher.html_generator import HtmlGenerator
from src.publisher.affiliate import AffiliateInjector

def main():
    parser = argparse.ArgumentParser(description="Gaia Content Automation")
    parser.add_argument("--topic", type=str, required=True, help="Topic to write about")
    parser.add_argument("--type", type=str, default="article", choices=["article", "news"], help="Type of content")
    args = parser.parse_args()

    print(f"Starting Gaia... Topic: {args.topic}")

    # 1. Generate Content
    client = GeminiClient()
    prompt_template = Prompts.AFFILIATE_ARTICLE if args.type == "article" else Prompts.NEWS_SUMMARY
    prompt = prompt_template.format(topic=args.topic)

    print("Generating content with Gemini...")
    content = client.generate_content(prompt)

    if not content:
        print("Failed to generate content.")
        return

    # 2. Inject Affiliate Links
    print("Injecting affiliate links...")
    injector = AffiliateInjector(amazon_tag="demo-22", rakuten_id="demo-11")
    
    # Inject search links at the bottom for now
    amz_link = injector.generate_search_link(args.topic, "amazon")
    rak_link = injector.generate_search_link(args.topic, "rakuten")
    
    links_md = f"\n\n## 価格をチェックする\n- [Amazonで見る]({amz_link})\n- [楽天で見る]({rak_link})"
    content = injector.inject_links(content + links_md)

    # 3. Publish Content
    print("Publishing content...")
    generator = HtmlGenerator()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"article_{timestamp}.html"
    
    # Extract title
    title = args.topic
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line.replace('# ', '').strip()
            break
    
    filepath = generator.generate_article(title, content, filename)
    
    # Update Index
    generator.update_index()
    
    print(f"Done! Article generated at: {filepath}")

if __name__ == "__main__":
    main()
