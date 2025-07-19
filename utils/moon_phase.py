from skyfield import almanac

def get_moon_phase(eph, t):
    phase = almanac.moon_phase(eph, t)
    deg = phase.degrees % 360

    if deg < 45:
        return "🌑 Новолуние"
    elif deg < 90:
        return "🌒 Растущий полумесяц"
    elif deg < 135:
        return "🌓 Первая четверть"
    elif deg < 180:
        return "🌔 Почти полнолуние"
    elif deg < 225:
        return "🌕 Полнолуние"
    elif deg < 270:
        return "🌖 Убывающее"
    elif deg < 315:
        return "🌗 Последняя четверть"
    else:
        return "🌘 Стареющий серп"
