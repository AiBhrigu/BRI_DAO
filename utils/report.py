# utils/report.py
import os

def save_report(date_str, moon_phase, positions, aspects):
    output = f"# Астрологический отчёт на {date_str}\n\n"
    output += f"## Фаза Луны: {moon_phase}\n\n"
    output += "## Положение планет:\n"
    for planet, pos in positions.items():
        output += f"- {planet.title()}: {pos['degree']}° {pos['sign']}\n"

    output += "\n## Аспекты:\n"
    if aspects:
        for asp in aspects:
            output += f"- {asp['planet1']} — {asp['aspect']} — {asp['planet2']} ({asp['angle']}°)\n"
    else:
        output += "### Нет значимых аспектов\n"

    os.makedirs("docs/history", exist_ok=True)
    with open(f"docs/history/{date_str}.md", "w") as f:
        f.write(output)
