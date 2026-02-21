import os
import re

def main():
    docs_dir = 'docs'
    count = 0
    for filename in os.listdir(docs_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'rel="icon"' in content or 'favicon.png' in content:
            continue
            
        # Add favicon after <title>
        new_content = re.sub(
            r'(<title>.*?</title>)',
            r'\1\n            <link rel="icon" href="favicon.png" type="image/png">',
            content,
            count=1,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            
    print(f"Added favicon to {count} files.")

if __name__ == '__main__':
    main()
