import os
import csv
from datetime import datetime

LOG_FILE = "logs/history.csv"

def log_generation(count, mode):
    """
    Logs a generation event to history.csv.
    
    Args:
        count (int): Number of articles generated.
        mode (str): Mode of generation (e.g., "Bulk", "Single", "RegenerateAll").
    """
    # Ensure logs directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Check if file exists to write header
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Count', 'Mode'])
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, count, mode])
        print(f"Logged generation event: {timestamp}, {count} articles, Mode: {mode}")
