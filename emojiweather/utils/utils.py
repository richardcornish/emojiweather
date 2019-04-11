from django.contrib.gis.geoip2 import GeoIP2

from geoip2.errors import GeoIP2Error
from ipware.ip import get_real_ip


def get_location_from_ip(request):
    ip = get_real_ip(request)
    if ip:
        g = GeoIP2()
        try:
            record = g.city(ip)
        except GeoIP2Error:
            return None
        if record:
            city = record['city'] if 'city' in record and record['city'] else ''
            country = record['country_name'] if 'country_name' in record and record['country_name'] else ''
            delimeter = ', ' if city and country else ''
            return '%s%s%s' % (city, delimeter, country)
    return None
