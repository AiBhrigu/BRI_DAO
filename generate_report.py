import json
from datetime import datetime

with open("output.json", "r") as f:
    data = json.load(f)

timestamp = data["timestamp"]
planets = data["planets"]
aspects = data["aspects"]

# Формируем markdown
lines = [f"# 🔭 Эфемериды на {timestamp}\n"]

# Планеты
lines.append("## 🌞 Планеты\n")
for name, info in planets.items():
    if name == "moon":
        continue
    lines.append(f"- **{name.title()}**: {info['sign']} {info['degree']}°")

# Луна
lines.append("\n## 🌙 Лунная Фаза\n")
lines.append(f"- **Фаза**: {planets['moon']['phase']}")
lines.append(f"- **Освещенность**: {planets['moon']['illumination']}%")

# Аспекты
lines.append("\n## ⚡ Аспекты\n")
for asp in aspects:
    lines.append(f"- **{asp['planet1'].title()}** {asp['aspect']} **{asp['planet2'].title()}** (угол: {asp['angle']}°)")

# Сохраняем в docs/
with open("docs/report.md", "w") as f:
    f.write("\n".join(lines))

print("✅ Markdown-отчёт сохранён в docs/report.md")
