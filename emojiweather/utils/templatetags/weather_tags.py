import json
import os
import random

from django import template

from ua_parser import user_agent_parser

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
register = template.Library()


@register.simple_tag
def get_location():
    locations = [
        {'title': 'Wrigley Field', 'code': 'US'},
        {'title': 'Walt Disney World', 'code': 'US'},
        {'title': 'Statue of Liberty', 'code': 'US'},
        {'title': 'Hollywood', 'code': 'US'},
        {'title': 'The White House', 'code': 'US'},
        {'title': 'Buckingham Palace', 'code': 'GB'},
        {'title': 'The Eiffel Tower', 'code': 'FR'},
        {'title': 'The Great Pyramid of Egypt', 'code': 'EG'},
        {'title': 'The Forbidden City', 'code': 'CN'},
        {'title': 'The Great Barrier Reef', 'code': 'AU'},
        {'title': 'Mount Everest', 'code': 'NP'},
        {'title': 'Antarctica', 'code': 'AQ'},
    ]
    location = random.choice(locations)
    path = os.path.join(BASE_DIR, 'data', 'flags.json')
    with open(path, 'r') as f:
        data = json.load(f)
        for icon in data:
            if icon['code'] == location['code']:
                emoji = icon['html']
    return {
        'title': location['title'],
        'emoji': emoji,
        'query': quote_plus(location['title'].lower()),
    }


@register.simple_tag(takes_context=True)
def get_os(context):
    request = context['request']
    ua = request.META['HTTP_USER_AGENT']
    os = user_agent_parser.ParseOS(ua)
    return os.get('family', '')


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
        if value:
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


@register.filter(name='quote_plus')
def _quote_plus(value):
    return quote_plus(value)


@register.tag
def strip(parser, token):
    nodelist = parser.parse(('endstrip',))
    parser.delete_first_token()
    return StripNode(nodelist)

class StripNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return " ".join(output.split())
