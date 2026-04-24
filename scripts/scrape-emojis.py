#!/usr/bin/env python3
"""
Scrape emoji data from the Unicode emoji list and generate JSON for the site.

Rows on unicode.org/emoji/charts/full-emoji-list.html follow a fixed shape:
  td.code  — codepoints, e.g. "U+1F600" or "U+1F636 U+200D U+1F32B U+FE0F"
  td.chars — the rendered glyph (can be absent from unicode.org's server font)
  td.name  — CLDR short name, prefixed with "⊛ " when unicode.org can't render it

We build the emoji from td.code so we always get the real character, even for
glyphs unicode.org itself can't render (e.g. trombone in Unicode 16).
"""

import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://unicode.org/emoji/charts/full-emoji-list.html"


def codepoints_to_char(code_text: str) -> str:
    """Convert "U+1F636 U+200D U+1F32B U+FE0F" into the actual emoji string."""
    parts = code_text.split()
    chars = []
    for part in parts:
        if not part.startswith("U+"):
            raise ValueError(f"unexpected codepoint token: {part!r}")
        chars.append(chr(int(part[2:], 16)))
    return "".join(chars)


def scrape_emojis():
    print(f"Fetching emoji data from {URL}...")
    response = requests.get(URL, timeout=60)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    emojis = []

    for row in soup.find_all("tr"):
        code_cell = row.find("td", class_="code")
        name_cell = row.find("td", class_="name")
        if not (code_cell and name_cell):
            continue

        code = code_cell.get_text(strip=True)
        name = name_cell.get_text(strip=True)
        if not code or not name:
            continue

        # Strip unicode.org's "glyph not in our font" marker from the name.
        if name.startswith("⊛"):
            name = name.lstrip("⊛").strip()

        try:
            emoji = codepoints_to_char(code)
        except ValueError as e:
            print(f"  skipping row: {e}")
            continue

        emojis.append({"emoji": emoji, "name": name})

    print(f"Found {len(emojis)} emojis")
    return emojis


def deduplicate_emojis(emojis):
    seen = set()
    unique = []
    for item in emojis:
        if item["emoji"] in seen:
            continue
        seen.add(item["emoji"])
        unique.append(item)
    print(f"Deduplicated to {len(unique)} unique emojis")
    return unique


def save_emojis(emojis, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(emojis, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(emojis)} emojis to {output_path}")


def main():
    project_root = Path(__file__).parent.parent
    json_output = project_root / "src" / "data" / "emojis.json"
    json_output.parent.mkdir(parents=True, exist_ok=True)

    emojis = scrape_emojis()
    unique_emojis = deduplicate_emojis(emojis)
    save_emojis(unique_emojis, json_output)

    print("\nDone!")
    print(f"  - {json_output}")
    print(f"\nTotal emojis: {len(unique_emojis)}")


if __name__ == "__main__":
    main()
