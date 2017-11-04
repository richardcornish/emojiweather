import json
import os

from django import template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
register = template.Library()


@register.filter
def iconify(value):
    path = os.path.join(BASE_DIR, 'data', 'icons.json')
    with open(path, 'r') as f:
        data = json.load(f)
        return data[value] or data['unknown']


@register.filter
def moonify(value):
    path = os.path.join(BASE_DIR, 'data', 'moons.json')
    with open(path, 'r') as f:
        data = json.load(f)
        percentage = value * 100
        if 0 <= percentage < 6.25 or 93.75 <= percentage <= 100:
            return data['new-moon']
        elif 6.25 <= percentage < 18.75:
            return data['waxing-crescent']
        elif 18.75 <= percentage < 31.25:
            return data['first-quarter']
        elif 31.25 <= percentage < 43.75:
            return data['waxing-gibbous']
        elif 43.75 <= percentage < 56.25:
            return data['full-moon']
        elif 56.25 <= percentage < 68.75:
            return data['waning-gibbous']
        elif 68.75 <= percentage < 81.25:
            return data['last-quarter']
        elif 81.25 <= percentage < 93.75:
            return data['waning-crescent']
        else:
            return data['unknown']


@register.filter
def flagify(value):
    path = os.path.join(BASE_DIR, 'data', 'flags.json')
    with open(path, 'r') as f:
        data = json.load(f)
        for v in value:
            for key in v:
                if key == 'types':
                    for t in v['types']:
                        if t == 'country':
                            code = v['short_name']
                            for c in data:
                                if c == code.lower():
                                    return data[c]
