#!/usr/bin/env python3
import sys
import os
import datetime

def create_diary_entry(title):
    # Get current date
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    date_str = now.strftime('%Y-%m-%d')
    
    # Base directory is the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, year, month, day)
    
    # Create directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Format: YYYY-MM-DD Title.md
    filename = f"{date_str} {title}.md"
    filepath = os.path.join(target_dir, filename)
    
    if os.path.exists(filepath):
        print(f"Error: File '{filename}' already exists.")
        return
        
    # Create the file with a title header
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        
    print(f"Created: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 new_entry.py <title>")
        sys.exit(1)
    
    # Join arguments to allow titles without quotes if typical shell words
    # But usually better to require quotes for complex titles.
    # Handling simple space-separated args as one title just in case.
    title = " ".join(sys.argv[1:])
    
    create_diary_entry(title)
