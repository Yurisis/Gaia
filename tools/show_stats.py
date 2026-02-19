import os
import csv
from datetime import datetime, timedelta

DOCS_DIR = "docs"
LOG_FILE = "logs/history.csv"

def get_total_articles():
    if not os.path.exists(DOCS_DIR):
        return 0
    return len([f for f in os.listdir(DOCS_DIR) if f.endswith(".html") and f != "index.html" and not f.startswith("google") and not f.startswith("test_")])

def get_daily_stats():
    if not os.path.exists(DOCS_DIR):
        return {}
    
    stats = {}
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".html") and f != "index.html" and not f.startswith("google") and not f.startswith("test_")]
    
    count_today = 0
    count_yesterday = 0
    
    for f in files:
        filepath = os.path.join(DOCS_DIR, f)
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath)).date()
        
        if mtime == today:
            count_today += 1
        elif mtime == yesterday:
            count_yesterday += 1
            
    return {
        "Today": count_today,
        "Yesterday": count_yesterday
    }

def show_history(limit=10):
    if not os.path.exists(LOG_FILE):
        print("No execution history found.")
        return

    print(f"\n--- Execution History (Last {limit}) ---")
    print(f"{'Timestamp':<25} {'Count':<10} {'Mode':<15}")
    print("-" * 50)
    
    try:
        with open(LOG_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
            
            # Skip header if present
            if data and data[0][0] == 'Timestamp':
                data = data[1:]
                
            # Show last N
            for row in data[-limit:]:
                timestamp, count, mode = row
                print(f"{timestamp:<25} {count:<10} {mode:<15}")
    except Exception as e:
        print(f"Error reading history: {e}")

def main():
    print("\n=== Gaia Content Generation Stats ===\n")
    
    total = get_total_articles()
    print(f"Total Published Articles: {total}")
    
    daily = get_daily_stats()
    print(f"Generated Today:        {daily['Today']}")
    print(f"Generated Yesterday:    {daily['Yesterday']}")
    
    show_history()
    print("\n=====================================")

if __name__ == "__main__":
    main()
