# utils/history_index.py

import os

TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>История астрологических отчётов</title>
</head>
<body>
    <h1>🕰️ История отчётов</h1>
    <ul>
"""

TEMPLATE_FOOT = """    </ul>
</body>
</html>
"""

def generate_index(history_dir="docs/history"):
    entries = sorted([
        f for f in os.listdir(history_dir)
        if f.endswith(".md") and f != "index.html"
    ])
    
    with open(os.path.join(history_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(TEMPLATE_HEAD)
        for entry in entries:
            date = entry.replace(".md", "")
            f.write(f'        <li><a href="{entry}">{date}</a></li>\n')
        f.write(TEMPLATE_FOOT)
