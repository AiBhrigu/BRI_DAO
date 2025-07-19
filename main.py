from skyfield.api import load
from datetime import timedelta
import json
import math
from itertools import combinations

# Знаки Зодиака
zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# Основные аспекты
ASPECTS = [
    {"name": "Conjunction", "angle": 0,   "orb": 8},
    {"name": "Opposition",  "angle": 180, "orb": 8},
    {"name": "Trine",       "angle": 120, "orb": 6},
    {"name": "Square",      "angle": 90,  "orb": 6},
    {"name": "Sextile",     "angle": 60,  "orb": 4}
]

def zodiac(deg):
    return zodiac_signs[int(deg // 30)]

def moon_phase(moon, sun, t):
    elongation = sun.at(t).observe(moon).apparent().separation_from(
        sun.at(t).observe(sun).apparent()).degrees
    phase = (1 + math.cos(math.radians(elongation))) / 2
    if elongation < 10:
        return "New Moon", round(phase * 100)
    elif elongation < 90:
        return "Waxing Crescent", round(phase * 100)
    elif elongation < 135:
        return "First Quarter", round(phase * 100)
    elif elongation < 170:
        return "Waxing Gibbous", round(phase * 100)
    elif elongation < 190:
        return "Full Moon", round(phase * 100)
    elif elongation < 235:
        return "Waning Gibbous", round(phase * 100)
    elif elongation < 270:
        return "Last Quarter", round(phase * 100)
    else:
        return "Waning Crescent", round(phase * 100)

def angle_diff(a1, a2):
    diff = abs(a1 - a2) % 360
    return min(diff, 360 - diff)

def find_aspect(diff):
    for asp in ASPECTS:
        if abs(diff - asp["angle"]) <= asp["orb"]:
            return asp["name"]
    return None

# Загрузка эфемерид
eph = load('de421.bsp')
ts = load.timescale()
t = ts.now()
earth = eph['earth']

# Планеты
bodies = {
    'sun': eph['sun'],
    'moon': eph['moon'],
    'mercury': eph['mercury'],
    'venus': eph['venus'],
    'mars': eph['mars'],
    'jupiter': eph['jupiter barycenter'],
    'saturn': eph['saturn barycenter'],
    'uranus': eph['uranus barycenter'],
    'neptune': eph['neptune barycenter'],
    'pluto': eph['pluto barycenter']
}

# Расчёт долготы всех планет
planet_positions = {}
for name, body in bodies.items():
    astrometric = earth.at(t).observe(body).apparent()
    lon = astrometric.ecliptic_latlon()[1].degrees % 360
    planet_positions[name] = lon

# Формируем основную структуру
data = {
    'timestamp': t.utc_strftime(),
    'planets': {},
    'aspects': []
}

# Добавляем данные по планетам
for name, lon in planet_positions.items():
    data['planets'][name] = {
        'sign': zodiac(lon),
        'degree': round(lon % 30, 2)
    }

# Фаза Луны
phase_name, illumination = moon_phase(bodies['moon'], bodies['sun'], t)
data['planets']['moon']['phase'] = phase_name
data['planets']['moon']['illumination'] = illumination

# Вычисляем аспекты между всеми парами
for p1, p2 in combinations(planet_positions.keys(), 2):
    diff = angle_diff(planet_positions[p1], planet_positions[p2])
    aspect = find_aspect(diff)
    if aspect:
        data['aspects'].append({
            'planet1': p1,
            'planet2': p2,
            'angle': round(diff, 2),
            'aspect': aspect
        })

# Сохраняем в файл
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Эфемериды + аспекты успешно сохранены в output.json")
