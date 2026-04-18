#!/usr/bin/env python3
"""
Scrape emoji data from Unicode emoji list and generate JSON for React app.
"""

import json
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Unicode emoji list URL
URL = "https://unicode.org/emoji/charts/full-emoji-list.html"

def scrape_emojis():
    """Fetch and parse emoji data from Unicode website."""
    print(f"Fetching emoji data from {URL}...")
    
    response = requests.get(URL)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    emojis = []
    
    # Find all table rows
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows:
            # Get all cells in this row
            cells = row.find_all('td')
            
            # Skip if not enough cells
            if len(cells) < 5:
                continue
            
            try:
                # Look for the emoji character - it should be in one of the cells
                # and should be a non-ASCII character
                emoji = None
                name = None
                
                for i, cell in enumerate(cells):
                    text = cell.get_text(strip=True)
                    
                    # Look for emoji (non-ASCII single/multi char)
                    if text and text != '—' and any(ord(c) > 127 for c in text):
                        # This might be the emoji
                        if len(text) <= 10:  # Emoji shouldn't be too long
                            emoji = text
                    
                    # The last cell typically has the name
                    if i == len(cells) - 1 and text and text != '—':
                        # Make sure it's not a number or code
                        if not text.startswith('U+') and not text.isdigit():
                            name = text
                
                if emoji and name:
                    # Clean up the name
                    name = name.replace('⊛ ', '').strip()
                    emojis.append({
                        'emoji': emoji,
                        'name': name
                    })
                    
            except Exception as e:
                continue
    
    print(f"Found {len(emojis)} emojis")
    return emojis

def deduplicate_emojis(emojis):
    """Remove duplicate emojis, keeping first occurrence."""
    seen = set()
    unique = []
    
    for emoji_data in emojis:
        emoji_char = emoji_data['emoji']
        if emoji_char not in seen:
            seen.add(emoji_char)
            unique.append(emoji_data)
    
    print(f"Deduplicated to {len(unique)} unique emojis")
    return unique

def save_emojis(emojis, output_path):
    """Save emojis to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(emojis, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(emojis)} emojis to {output_path}")

def generate_ts_file(emojis, output_path):
    """Generate TypeScript file from emojis."""
    ts_content = "const emojis = " + json.dumps(emojis, ensure_ascii=False, indent=2) + ";\n\nexport default emojis;\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    print(f"Generated TypeScript file: {output_path}")

def main():
    # Paths
    project_root = Path(__file__).parent.parent
    json_output = project_root / 'public' / 'emojis.json'
    ts_output = project_root / 'src' / 'emojis.ts'
    
    # Scrape
    emojis = scrape_emojis()
    
    # Deduplicate
    unique_emojis = deduplicate_emojis(emojis)
    
    # Save as JSON for the web app to load
    save_emojis(unique_emojis, json_output)
    
    # Also generate TypeScript file (for direct import if preferred)
    generate_ts_file(unique_emojis, ts_output)
    
    print("\nDone! You now have:")
    print(f"  - {json_output} (for dynamic loading)")
    print(f"  - {ts_output} (for direct import)")
    print(f"\nTotal emojis: {len(unique_emojis)}")

if __name__ == '__main__':
    main()
