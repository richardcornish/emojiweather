import json
import os

from django import template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
register = template.Library()


@register.filter
def weatherify(value):
    path = os.path.join(BASE_DIR, 'data', 'weather.json')
    with open(path, 'r') as f:
        data = json.load(f)
        for icon in data:
            if icon['slug'] == value:
                return icon


@register.filter
def moonify(value):
    path = os.path.join(BASE_DIR, 'data', 'moons.json')
    with open(path, 'r') as f:
        data = json.load(f)
        percentage = value * 100
        for icon in data:
            if icon['start'] <= percentage < icon['finish']:
                return icon


@register.filter
def flagify(value):
    path = os.path.join(BASE_DIR, 'data', 'flags.json')
    with open(path, 'r') as f:
        data = json.load(f)
        # loop through json
        for component in value:
            for t in component['types']:
                if t == 'country':
                    # loop through flags
                    for icon in data:
                        if icon['code'] == component['short_name']:
                            return icon
