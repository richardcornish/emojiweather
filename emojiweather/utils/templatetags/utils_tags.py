import json
import os
import random
from datetime import date

from django import template
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe

import pytz
from dateutil.easter import easter
from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE, relativedelta as rd
from ua_parser import user_agent_parser

try:
    from urllib import quote_plus as _quote_plus
except ImportError:
    from urllib.parse import quote_plus as _quote_plus

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

register = template.Library()


@register.simple_tag
def get_location():
    locations = [
        {'title': 'Spotted Lake', 'code': 'CA'},
        {'title': 'The Giant’s Causeway', 'code': 'GB'},
        {'title': 'Thor’s Well', 'code': 'US'},
        {'title': 'Pamukkale', 'code': 'TR'},
        {'title': 'Lake Hillier', 'code': 'AU'},
        {'title': 'Badab-e-Surt', 'code': 'IR'},
        {'title': 'Tianzi mountains', 'code': 'CN'},
        {'title': 'Nasca Lines', 'code': 'PE'},
        {'title': 'Bermuda Triangle', 'code': 'BM'},
        {'title': 'Socotra Island', 'code': 'YE'},
        {'title': 'The Hand', 'code': 'CL'},
        {'title': 'Chocolate Hills of Bohol Island', 'code': 'PH'},
        {'title': 'Red Beach', 'code': 'CN'},
        {'title': 'Plain of Jars', 'code': 'LA'},
        {'title': 'Goblin Valley State Park', 'code': 'US'},
        {'title': 'Whale Bone Alley', 'code': 'RU'},
        {'title': 'Glass Beach', 'code': 'US'},
        {'title': 'Catacombs', 'code': 'FR'},
        {'title': 'Fly Geyser', 'code': 'US'},
        {'title': 'Cat Island', 'code': 'JP'},
        {'title': 'Strokkur Geyser', 'code': 'IS'},
        {'title': 'French Quarter', 'code': 'US'},
        {'title': 'Lake Tahoe', 'code': 'US'},
        {'title': 'Pike Place Market', 'code': 'US'},
        {'title': 'Badlands National Park', 'code': 'US'},
        {'title': 'Fenway Park', 'code': 'US'},
        {'title': 'Powell’s City of Books', 'code': 'US'},
        {'title': 'Millennium Park', 'code': 'US'},
        {'title': 'Golden Gate Bridge', 'code': 'US'},
        {'title': 'Griffith Observatory', 'code': 'US'},
        {'title': 'Grand Canyon', 'code': 'US'},
        {'title': 'South Beach', 'code': 'US'},
        {'title': 'Central Park', 'code': 'US'},
        {'title': 'Times Square', 'code': 'US'},
        {'title': 'Las Vegas Strip', 'code': 'US'},
        {'title': 'Niagara Falls', 'code': 'CA'},
        {'title': 'Yellowstone National Park', 'code': 'US'},
        {'title': 'Death Valley', 'code': 'US'},
        {'title': 'Mount Rushmore', 'code': 'US'},
        {'title': 'Yosemite National Park', 'code': 'US'},
        {'title': 'Jackson Hole', 'code': 'US'},
        {'title': 'The Smithsonian', 'code': 'US'},
        {'title': 'Waikiki Beach', 'code': 'US'},
        {'title': 'The MET', 'code': 'US'},
        {'title': 'Redwood National Park', 'code': 'US'},
        {'title': 'The Second City', 'code': 'US'},
        {'title': 'Alcatraz Island', 'code': 'US'},
        {'title': 'Wrigley Field', 'code': 'US'},
        {'title': 'Walt Disney World', 'code': 'US'},
        {'title': 'Statue of Liberty', 'code': 'US'},
        {'title': 'Hollywood', 'code': 'US'},
        {'title': 'The White House', 'code': 'US'},
        {'title': 'Buckingham Palace', 'code': 'GB'},
        {'title': 'Eiffel Tower', 'code': 'FR'},
        {'title': 'Great Pyramid of Giza', 'code': 'EG'},
        {'title': 'Forbidden City', 'code': 'CN'},
        {'title': 'Great Barrier Reef', 'code': 'AU'},
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
        'query': _quote_plus(location['title'].lower()),
    }


@register.simple_tag(takes_context=True)
def get_os(context):
    request = context['request']
    ua = request.META['HTTP_USER_AGENT']
    os = user_agent_parser.ParseOS(ua)
    return os.get('family', '')


@register.simple_tag
def get_holidays(tz):
    # Get today
    timezone.activate(pytz.timezone(tz))
    now = timezone.localtime(timezone.now())
    today = now.date()
    year = today.year
    # Compute holidays
    holidays = []
    rd_weekdays = {
        'Monday': MO,
        'Tuesday': TU,
        'Wednesday': WE,
        'Thursday': TH,
        'Friday': FR,
        'Saturday': SA,
        'Sunday': SU,
    }
    path = os.path.join(BASE_DIR, 'data', 'holidays.json')
    with open(path, 'r') as f:
        data = json.load(f)
        for item in data:
            # Copy data
            holiday = item.copy()
            # Easter
            if item['name'] == 'Easter':
                holiday['date'] = easter(year)
            else:
                # Absolute holiday
                holiday['date'] = date(year, item['month'], item['day'])
                # Relative holiday
                if 'weekday' in item and item['weekday'] and 'week' in item and item['week']:
                    holiday['date'] += rd(weekday=rd_weekdays[item['weekday']](item['week']))
                    # Election Day
                    if 'days' in item and item['days']:
                        holiday['date'] += rd(days=item['days'])
            holidays.append(holiday)
    return [h for h in holidays if h['date'] == today]


@register.filter
def weatherify(value):
    path = os.path.join(BASE_DIR, 'data', 'weather.json')
    with open(path, 'r') as f:
        data = json.load(f)
        for item in data:
            if item['slug'] == value:
                return item


@register.filter
def moonify(value):
    path = os.path.join(BASE_DIR, 'data', 'moons.json')
    with open(path, 'r') as f:
        data = json.load(f)
        if value:
            percentage = value * 100
            for item in data:
                try:
                    if item['start'] <= percentage < item['finish']:
                        return item
                except:
                    return {}


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
                    for item in data:
                        if item['code'] == component['short_name']:
                            return item


@register.simple_tag
def get_google_maps_key():
    return getattr(settings, 'GOOGLE_MAPS_API_KEY', '')


@register.filter
def roundify(value):
    return round(value)


@register.filter
def minusify(value):
    return mark_safe(str(value).replace('-', '&#8722;'))


@register.filter
def curlify(value):
    return mark_safe(value.replace("'", '&#8217;'))


@register.filter
def quote_plus(value):
    return _quote_plus(value)


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
        return ' '.join(output.split())
