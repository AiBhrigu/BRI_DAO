# main.py
import argparse
from datetime import datetime
from utils.ephemeris import get_planet_positions, get_aspects
from utils.moon_phase import get_moon_phase
from utils.report import save_report
from skyfield.api import load

parser = argparse.ArgumentParser()
parser.add_argument('--date', help='Date in YYYY-MM-DD format', default=None)
args = parser.parse_args()

# Дата: либо из аргумента, либо текущая
if args.date:
    date_str = args.date
else:
    date_str = datetime.utcnow().strftime('%Y-%m-%d')

eph = load('de430t.bsp')
ts = load.timescale()
t = ts.utc(*map(int, date_str.split('-')))

positions = get_planet_positions(t, eph)
aspects = get_aspects(positions)
moon_phase_name = get_moon_phase(eph, t)

save_report(date_str, moon_phase_name, positions, aspects)
print("✅ Markdown-отчёт сохранён в docs/history/{}.md".format(date_str))
