from django import template

register = template.Library()


@register.filter
def iconify(value):
    icons = {
        'clear-day': '\u2600',
        'clear-night': '\U0001F30C',
        'rain': '\U0001F327',
        'snow': '\u2744',
        'sleet': '\U0001F328',
        'wind': '\U0001F32C',
        'fog': '\U0001F32B',
        'cloudy': '\u2601',
        'partly-cloudy-day': '\u26C5',
        'partly-cloudy-night': '\u2601\U0001F30C',
        'hail': '\U0001F327',
        'thunderstorm': '\u26C8',
        'tornado': '\U0001F32A',
    }
    return icons.get(value, '¯\_(ツ)_/¯')


@register.filter
def moonify(value):
    phases = {
        'new-moon': {
            'name': 'New moon',
            'icon': '\U0001F311',
        },
        'waxing-crescent': {
            'name': 'Waxing Crescent',
            'icon': '\U0001F312',
        },
        'first-quarter': {
            'name': 'First Quarter',
            'icon': '\U0001F313',
        },
        'waxing-gibbous': {
            'name': 'Waxing Gibbous',
            'icon': '\U0001F314',
        },
        'full-moon': {
            'name': 'Full Moon',
            'icon': '\U0001F315',
        },
        'waning-gibbous': {
            'name': 'Waning Gibbous',
            'icon': '\U0001F316',
        },
        'last-quarter': {
            'name': 'Last Quarter',
            'icon': '\U0001F317',
        },
        'waning-crescent': {
            'name': 'Waning Crescent',
            'icon': '\U0001F318',
        },
        'unknown': {
            'name': 'Unknown moon',
            'icon': '¯\_(ツ)_/¯',
        },
    }
    percentage = value * 100
    if 0 <= percentage < 6.25 or 93.75 <= percentage <= 100:
        return phases['new-moon']
    elif 6.25 <= percentage < 18.75:
        return phases['waxing-crescent']
    elif 18.75 <= percentage < 31.25:
        return phases['first-quarter']
    elif 31.25 <= percentage < 43.75:
        return phases['waxing-gibbous']
    elif 43.75 <= percentage < 56.25:
        return phases['full-moon']
    elif 56.25 <= percentage < 68.75:
        return phases['waning-gibbous']
    elif 68.75 <= percentage < 81.25:
        return phases['last-quarter']
    elif 81.25 <= percentage < 93.75:
        return phases['waning-crescent']
    else:
        return phases['unknown']
