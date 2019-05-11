from django.contrib.gis.geoip2 import GeoIP2

from geoip2.errors import GeoIP2Error
from ipware import get_client_ip


def get_location_from_ip(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is not None:
        g = GeoIP2()
        try:
            record = g.city(client_ip)
        except GeoIP2Error:
            return None
        if record:
            city = record.get('city') or ''
            country = record.get('country') or ''
            delimeter = ', ' if city and country else ''
            return f'{city}{delimeter}{country}'
    return None
