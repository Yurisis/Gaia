import re

class AffiliateInjector:
    def __init__(self, amazon_tag=None, rakuten_id=None):
        self.amazon_tag = amazon_tag or "no_tag"
        self.rakuten_id = rakuten_id or "no_id"

    def inject_links(self, content):
        """
        Scans content for product names and injects affiliate links.
        For now, this is a placeholder that appends a generic disclaimer and 
        example links. In a real scenario, this would use a product API 
        or a pre-defined dictionary of links.
        """
        
        # Simple keywords to link (Demo purpose)
        # In reality, you'd use the Amazon Product Advertising API
        
        disclaimer = "\n\n---\n*本記事はアフィリエイト・プロモーションを含みます。*\n"
        
        # Example of replacing a generic marker (if we instructed Gemini to leave one)
        # Or just appending a search link for the topic
        
        return content + disclaimer

    def generate_search_link(self, keyword, platform="amazon"):
        if platform == "amazon":
            return f"https://www.amazon.co.jp/s?k={keyword}&tag={self.amazon_tag}"
        elif platform == "rakuten":
            return f"https://search.rakuten.co.jp/search/mall/{keyword}/?afid={self.rakuten_id}"
        return "#"
