import os
import markdown
import re
from datetime import datetime

class HtmlGenerator:
    def __init__(self, output_dir="docs", base_url="https://yurisis.github.io/Gaia"):
        self.output_dir = output_dir
        self.base_url = base_url
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_article(self, title, markdown_content, filename):
        """Converts Markdown to HTML and saves it."""
        
        # Process Shortcodes before Markdown conversion
        processed_content = self.process_shortcodes(markdown_content)

        # Enable attribute lists extension if needed
        html_content = markdown.markdown(processed_content, extensions=['extra'])
        
        # OGP Description (First 100 chars of content, roughly)
        # Strip HTML tags for description if possible, or just use title
        description = f"{title}に関する詳細記事です。"
        
        # Article URL
        article_url = f"{self.base_url}/{filename}"

        template = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="description" content="{description}">
            
            <!-- OGP Tags -->
            <meta property="og:title" content="{title}" />
            <meta property="og:type" content="article" />
            <meta property="og:url" content="{article_url}" />
            <meta property="og:description" content="{description}" />
            <meta property="og:site_name" content="Gaia Blog" />
            <meta property="og:locale" content="ja_JP" />

            <style>
                /* Common */
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
                h1 {{ color: #2c3e50; font-size: 1.8em; margin-bottom: 30px; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; margin-top: 40px; font-size: 1.5em; clear: both; }}
                h3 {{ color: #2c3e50; margin-top: 30px; font-size: 1.25em; border-left: 5px solid #3498db; padding-left: 10px; }}
                a {{ color: #3498db; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .container {{ background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
                .footer {{ margin-top: 60px; padding-top: 20px; border-top: 1px solid #eee; font-size: 0.9em; color: #7f8c8d; text-align: center; }}
                .nav {{ margin-bottom: 20px; }}

                /* Chat Bubble */
                .chat-box {{ width: 100%; overflow: hidden; margin-bottom: 20px; }}
                .chat-face {{ float: left; margin-right: 15px; text-align: center; width: 60px; }}
                .chat-face img {{ width: 50px; height: 50px; border-radius: 50%; border: 2px solid #eee; object-fit: cover; background-color: #ddd; }}
                .chat-area {{ float: left; position: relative; width: calc(100% - 90px); }}
                .chat-bubble {{ position: relative; display: inline-block; padding: 15px; background: #f0f4f8; border-radius: 10px; }}
                .chat-bubble::after {{ content: ''; position: absolute; left: -10px; top: 15px; border-right: 15px solid #f0f4f8; border-top: 10px solid transparent; border-bottom: 10px solid transparent; }}
                
                /* Right Chat (User) */
                .chat-box.right .chat-face {{ float: right; margin-right: 0; margin-left: 15px; }}
                .chat-box.right .chat-area {{ float: right; text-align: right; }}
                .chat-box.right .chat-bubble {{ background: #e3f2fd; text-align: left; }}
                .chat-box.right .chat-bubble::after {{ left: auto; right: -10px; border-right: none; border-left: 15px solid #e3f2fd; }}

                /* Merit/Demerit Boxes */
                .box-common {{ padding: 20px; border-radius: 5px; margin: 25px 0; border: 1px solid transparent; }}
                .merit-box {{ background-color: #f0f9ff; border-color: #bae6fd; color: #0369a1; }}
                .merit-box::before {{ content: '✅ メリット'; display: block; font-weight: bold; margin-bottom: 10px; font-size: 1.1em; }}
                .demerit-box {{ background-color: #fef2f2; border-color: #fecaca; color: #b91c1c; }}
                .demerit-box::before {{ content: '⚠️ デメリット・注意点'; display: block; font-weight: bold; margin-bottom: 10px; font-size: 1.1em; }}

                /* Rating */
                .rating-box {{ display: flex; align-items: center; margin-bottom: 20px; font-weight: bold; background: #fffbeb; padding: 10px; border-radius: 5px; }}
                .stars {{ color: #f59e0b; font-size: 1.2em; margin-left: 10px; letter-spacing: 2px; }}

                /* Product Card (Amazon/Rakuten Style) */
                .product-card {{ display: flex; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; margin: 30px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); transition: transform 0.2s; }}
                .product-card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }}
                .product-img {{ width: 120px; background: #f3f4f6; display: flex; align-items: center; justify-content: center; font-size: 2em; color: #9ca3af; min-height: 120px; text-align: center; }}
                .product-info {{ padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; }}
                .product-title {{ font-weight: bold; font-size: 1.1em; margin-bottom: 5px; color: #1f2937; }}
                .product-btn-group {{ margin-top: 15px; display: flex; gap: 10px; }}
                .btn {{ display: inline-block; padding: 10px 20px; border-radius: 4px; color: #fff; font-weight: bold; text-align: center; font-size: 0.9em; flex: 1; max-width: 150px; text-decoration: none; }}
                .btn-amazon {{ background-color: #f9ce56; color: #111; }}
                .btn-rakuten {{ background-color: #bf0000; }}
                .btn:hover {{ opacity: 0.9; text-decoration: none; }}

                /* Clearfix for floats */
                .clearfix::after {{ content: ""; clear: both; display: table; }}

                /* Responsive */
                @media (max-width: 600px) {{
                    .product-card {{ flex-direction: column; }}
                    .product-img {{ width: 100%; height: 150px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="nav"><a href="index.html">← Top Page</a></div>
                <h1>{title}</h1>
                {html_content}
                <div class="footer">
                    <p>&copy; {datetime.now().year} Gaia Automated Content. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"Article saved to: {filepath}")
        return filepath

    def process_shortcodes(self, content):
        """Replaces custom shortcodes with HTML structures."""
        
        # Chat Left (User)
        # Pattern: [[CHAT_L: message]]
        def repl_chat_l(match):
            msg = match.group(1)
            return f"""
<div class="chat-box">
    <div class="chat-face"><img src="https://api.dicebear.com/9.x/avataaars/svg?seed=Felix" alt="User"></div>
    <div class="chat-area">
        <div class="chat-bubble">{msg}</div>
    </div>
</div>
"""
        content = re.sub(r'\[\[CHAT_L:\s*(.*?)\]\]', repl_chat_l, content, flags=re.DOTALL)

        # Chat Right (Agent)
        # Pattern: [[CHAT_R: message]]
        def repl_chat_r(match):
            msg = match.group(1)
            return f"""
<div class="chat-box right">
    <div class="chat-face"><img src="https://api.dicebear.com/9.x/avataaars/svg?seed=Aneka" alt="Agent"></div>
    <div class="chat-area">
        <div class="chat-bubble">{msg}</div>
    </div>
</div>
"""
        content = re.sub(r'\[\[CHAT_R:\s*(.*?)\]\]', repl_chat_r, content, flags=re.DOTALL)

        return content

    def generate_sitemap(self):
        """Generates sitemap.xml."""
        files = [f for f in os.listdir(self.output_dir) if f.startswith("article_") and f.endswith(".html")]
        files.sort(reverse=True)

        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Add index
        sitemap_content += f"""    <url>
        <loc>{self.base_url}/index.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
"""

        for f in files:
            file_url = f"{self.base_url}/{f}"
            sitemap_content += f"""    <url>
        <loc>{file_url}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""
        
        sitemap_content += "</urlset>"
        
        with open(os.path.join(self.output_dir, "sitemap.xml"), 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        print("Updated sitemap.xml")

    def update_index(self):
        """Updates the index.html file with a nice grid layout."""
        files = [f for f in os.listdir(self.output_dir) if f.startswith("article_") and f.endswith(".html")]
        files.sort(reverse=True) # Newest first

        # Extract titles from files to display in index
        articles_data = []
        for f in files:
            path = os.path.join(self.output_dir, f)
            title = f # Default
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # regex to parse <title>...</title>
                    m = re.search(r'<title>(.*?)</title>', content)
                    if m:
                        title = m.group(1)
            except:
                pass
            
            # Create a clean date from filename if possible
            # article_20260217... -> 2026-02-17
            date_str = "2026"
            m_date = re.search(r'article_(\d{8})_', f)
            if m_date:
                d = m_date.group(1)
                date_str = f"{d[:4]}-{d[4:6]}-{d[6:]}"

            articles_data.append({'file': f, 'title': title, 'date': date_str})

        cards_html = ""
        for item in articles_data:
            cards_html += f"""
            <a href="{item['file']}" class="card">
                <div class="card-content">
                    <div class="card-date">{item['date']}</div>
                    <h2 class="card-title">{item['title']}</h2>
                    <div class="card-readmore">Read More →</div>
                </div>
            </a>
            """

        template = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Gaia Blog - Automated Tech & Life Hacks</title>
            <meta name="description" content="AIが自動生成する最新のガジェット・ライフハックブログ。">
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; background-color: #f4f6f8; color: #333; }}
                header {{ text-align: center; margin-bottom: 50px; padding: 40px 0; }}
                h1 {{ font-size: 2.5em; margin: 0; color: #2c3e50; }}
                p.subtitle {{ color: #7f8c8d; font-size: 1.1em; }}
                
                .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
                
                .card {{ background: #fff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); overflow: hidden; text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s; display: block; }}
                .card:hover {{ transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                
                .card-content {{ padding: 20px; }}
                .card-date {{ font-size: 0.85em; color: #95a5a6; margin-bottom: 10px; }}
                .card-title {{ font-size: 1.2em; margin: 0 0 15px 0; color: #2c3e50; line-height: 1.4; border: none; padding: 0; }}
                .card-readmore {{ color: #3498db; font-weight: bold; font-size: 0.9em; }}
                
                .footer {{ margin-top: 60px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.9em; color: #7f8c8d; text-align: center; }}
            </style>
        </head>
        <body>
            <header>
                <h1>Gaia Blog</h1>
                <p class="subtitle">Daily Tech trends & Life Hacks provided by AI</p>
            </header>
            
            <div class="grid">
                {cards_html}
            </div>
            
            <div class="footer">
                <p>&copy; {datetime.now().year} Gaia Automated Content. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        
        with open(os.path.join(self.output_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(template)
        print("Updated index.html with Grid Layout")
        
        # Also update sitemap whenever index is updated
        self.generate_sitemap()
