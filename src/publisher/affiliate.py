import re

class AffiliateInjector:
    def __init__(self, amazon_tag=None, rakuten_id=None):
        self.amazon_tag = amazon_tag or "no_tag"
        self.rakuten_id = rakuten_id or "no_id"

    def inject_links(self, content):
        """
        Scans content for product names and injects affiliate links.
        """
        
        # In a real scenario, you'd extract keywords. For now, we assume the whole article promotes one main thing or we just add a generic card at the bottom.
        # Let's try to extract the main topic from the content or just use a placeholder
        
        disclaimer = "\n\n<p style='font-size:0.8em; color:#777;'>*本記事はアフィリエイト・プロモーションを含みます。*</p>"
        
        # Create a generic product card HTML to append
        # We can't know the exact product image/title without an API, so we use placeholders or simple text.
        
        # We will try to find the "topic" if possible, or just use a generic call.
        # Since this method just takes 'content', it's hard to know the exact keyword unless passed.
        # But we can assume the caller might want to append links *after* this method returns.
        # Actually, main.py constructs the link markdown *before* calling this? 
        # No, main.py calls:
        # full_content = str(content) + links_md
        # full_content = injector.inject_links(full_content)
        
        # So we should actually CHANGE how main.py handles the links, or just styling the links here.
        # But wait, main.py appends markdown links:
        # links_md = f"\n\n## 価格をチェックする\n- [Amazonで見る]({amz_link})\n- [楽天で見る]({rak_link})"
        
        # We should probably change main.py to NOT append that markdown, but let affiliate.py handle the card generation?
        # Or we can just Regex replace the links in `content` with our card.
        
        # Let's just return content + disclaimer for now, and we will update main.py to use a new method `generate_product_card` instead of manually creating links_md.
        
        return content + disclaimer

    def generate_product_card(self, keyword):
        """Generates a HTML product card."""
        amz_link = self.generate_search_link(keyword, "amazon")
        rak_link = self.generate_search_link(keyword, "rakuten")
        
        card_html = f"""
<div class="product-card">
    <div class="product-img">📦</div>
    <div class="product-info">
        <div class="product-title">{keyword} (検索結果)</div>
        <div class="product-btn-group">
            <a href="{amz_link}" class="btn btn-amazon" target="_blank" onclick="gtag('event', 'click_amazon', {{'event_category': 'affiliate', 'event_label': '{keyword}'}})">Amazonで探す</a>
            <a href="{rak_link}" class="btn btn-rakuten" target="_blank" onclick="gtag('event', 'click_rakuten', {{'event_category': 'affiliate', 'event_label': '{keyword}'}})">楽天で探す</a>
        </div>
    </div>
</div>
"""
        return card_html

    def generate_search_link(self, keyword, platform="amazon"):
        if platform == "amazon":
            return f"https://www.amazon.co.jp/s?k={keyword}&tag={self.amazon_tag}"
        elif platform == "rakuten":
            return f"https://search.rakuten.co.jp/search/mall/{keyword}/?afid={self.rakuten_id}"
        return "#"
