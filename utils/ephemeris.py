from math import degrees
from utils.constants import ZODIAC_SIGNS, ASPECTS, ORBS

PLANET_IDS = {
    "sun": "SUN",
    "moon": "MOON",
    "mercury": 199,
    "venus": 299,
    "mars": 4,
    "jupiter": 5,
    "saturn": 6,
    "uranus": 7,
    "neptune": 8,
    "pluto": 9
}

def get_planet_positions(t, eph):
    positions = {}
    for name, target_id in PLANET_IDS.items():
        try:
            planet = eph[target_id]
        except KeyError:
            print(f"[⚠] Planet '{name}' not found in ephemeris.")
            continue
        astrometric = eph["earth"].at(t).observe(planet)
        ecliptic = astrometric.ecliptic_latlon()
        longitude = ecliptic[1].degrees % 360
        sign_index = int(longitude // 30)
        degree_in_sign = longitude % 30
        sign = ZODIAC_SIGNS[sign_index]
        positions[name] = {
            "sign": sign,
            "degree": round(degree_in_sign, 2),
            "longitude": round(longitude, 2)
        }
    return positions

def get_aspects(positions):
    aspects = []
    keys = list(positions.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            p1, p2 = keys[i], keys[j]
            lon1 = positions[p1]['longitude']
            lon2 = positions[p2]['longitude']
            angle = abs(lon1 - lon2)
            if angle > 180:
                angle = 360 - angle
            for aspect, exact in ASPECTS.items():
                if abs(angle - exact) <= ORBS[aspect]:
                    aspects.append({
                        "planet1": p1.title(),
                        "planet2": p2.title(),
                        "angle": round(angle, 2),
                        "aspect": aspect
                    })
    return aspects
