import os
from pathlib import Path

HISTORY_DIR = Path("docs/history")
INDEX_FILE = HISTORY_DIR / "index.html"

def generate_index():
    files = sorted(
        [f for f in HISTORY_DIR.glob("*.md") if f.name != "index.md"],
        reverse=True
    )

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")
        f.write("<meta charset='utf-8'>\n<title>История астрологических отчётов</title>\n")
        f.write("</head>\n<body>\n")
        f.write("<h1>🕰️ История астрологических отчётов</h1>\n<ul>\n")

        for file in files:
            date = file.stem
            f.write(f"<li><a href='{date}.md'>{date}</a></li>\n")

        f.write("</ul>\n</body>\n</html>\n")

if __name__ == "__main__":
    generate_index()

- name: 🕰️ Генерация архива истории
  run: python3 utils/history_index.py
