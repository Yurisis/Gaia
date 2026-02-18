from src.publisher.html_generator import HtmlGenerator

def rebuild():
    gen = HtmlGenerator()
    gen.update_index()
    gen.generate_sitemap()
    print("Rebuild Complete")

if __name__ == "__main__":
    rebuild()
