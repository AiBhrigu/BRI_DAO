from flask import Flask, request, render_template_string
from skyfield.api import load
from utils.ephemeris import get_planet_positions, get_aspects
from utils.moon_phase import get_moon_phase
from datetime import datetime

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Эфемериды</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>🔭 Астрологическая космограмма</h1>
    <form method="GET">
        <label for="date">Введите дату (ГГГГ-ММ-ДД):</label>
        <input type="date" id="date" name="date" value="{{ date }}">
        <button type="submit">Показать</button>
    </form>

    {% if positions %}
        <h2>🌞 Положение планет на {{ date }}</h2>
        <ul>
        {% for planet, info in positions.items() %}
            <li><strong>{{ planet.title() }}</strong>: {{ info.sign }} {{ info.degree }}°</li>
        {% endfor %}
        </ul>

        <h2>⚡ Аспекты</h2>
        <ul>
        {% for aspect in aspects %}
            <li><strong>{{ aspect.planet1 }}</strong> {{ aspect.aspect }} <strong>{{ aspect.planet2 }}</strong> (угол: {{ aspect.angle }}°)</li>
        {% endfor %}
        </ul>

        <h2>🌙 Фаза Луны</h2>
        <p><strong>Фаза:</strong> {{ moon_phase['phase'] }} | <strong>Освещенность:</strong> {{ moon_phase['illumination'] }}%</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    date_str = request.args.get("date")
    if not date_str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")

    ts = load.timescale()
    t = ts.utc(*map(int, date_str.split("-")))
    eph = load("de440.bsp")

    positions = get_planet_positions(t, eph)
    aspects = get_aspects(positions)
    moon_phase = get_moon_phase(t, eph)

    return render_template_string(TEMPLATE,
                                  date=date_str,
                                  positions=positions,
                                  aspects=aspects,
                                  moon_phase=moon_phase)

if __name__ == "__main__":
    app.run(debug=True)
