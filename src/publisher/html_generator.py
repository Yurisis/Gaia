import os
import markdown
import re
from datetime import datetime

class HtmlGenerator:
    def __init__(self, output_dir="docs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_article(self, title, markdown_content, filename):
        """Converts Markdown to HTML and saves it."""
        
        # Process Shortcodes before Markdown conversion
        processed_content = self.process_shortcodes(markdown_content)

        # Enable attribute lists extension if needed
        html_content = markdown.markdown(processed_content, extensions=['extra'])
        
        template = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="description" content="{title}に関する詳細記事です。">
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

    def update_index(self):
        """Updates the index.html file with a list of all articles."""
        files = [f for f in os.listdir(self.output_dir) if f.startswith("article_") and f.endswith(".html")]
        files.sort(reverse=True) # Newest first

        links = ""
        for f in files:
            links += f'<li><a href="{f}">{f}</a></li>\n'

        template = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Gaia Blog</title>
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                ul {{ list-style-type: none; padding: 0; }}
                li {{ margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 4px; }}
                a {{ text-decoration: none; color: #333; font-weight: bold; display: block; }}
                a:hover {{ color: #3498db; }}
            </style>
        </head>
        <body>
            <h1>Gaia Blog - Latest Articles</h1>
            <ul>
                {links}
            </ul>
        </body>
        </html>
        """
        
        with open(os.path.join(self.output_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(template)
        print("Updated index.html")
