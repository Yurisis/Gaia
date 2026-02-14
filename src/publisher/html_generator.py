import os
import markdown
from datetime import datetime

class HtmlGenerator:
    def __init__(self, output_dir="docs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_article(self, title, markdown_content, filename):
        """Converts Markdown to HTML and saves it."""
        
        html_content = markdown.markdown(markdown_content)
        
        template = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="description" content="{title}に関する詳細記事です。">
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; margin-top: 30px; }}
                a {{ color: #3498db; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .container {{ background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
                .footer {{ margin-top: 40px; font-size: 0.9em; color: #7f8c8d; text-align: center; }}
                .nav {{ margin-bottom: 20px; }}
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

    def update_index(self):
        """Updates the index.html file with a list of all articles."""
        files = [f for f in os.listdir(self.output_dir) if f.startswith("article_") and f.endswith(".html")]
        files.sort(reverse=True) # Newest first

        links = ""
        for f in files:
            # Ideally we would extract the title from the file, but for now we use the filename
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
