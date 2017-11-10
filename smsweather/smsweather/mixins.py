from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import requests


class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)


class WeatherMixin(object):
    def get_geocode(self, address):
        errors = {
            'zero_results': 'We\u2019re sorry, but we could not find that location.',
            'over_query_limit': 'We\u2019re sorry, but the request quota has been reached.',
            'request_denied': 'We\u2019re sorry, but your request was denied.',
            'invalid_request': 'We\u2019re sorry, but we could not find that location.',
            'unknown': 'We\u2019re sorry, but an error occurred.',
        }
        key = settings.GOOGLE_GEOCODING_API_KEY
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={'address': address, 'key': key})
        j = r.json()
        if j['status'] == 'OK':
            return j['results'][0]
        else:
            try:
                error = errors[j['status'].lower()]
            except KeyError:
                error = errors['unknown']
            return 'Beep boop. %s \U0001F916' % error

    def get_weather(self, geocode):
        key = settings.DARK_SKY_API_KEY
        latitude = geocode['geometry']['location']['lat']
        longitude = geocode['geometry']['location']['lng']
        units = 'us'
        r = requests.get('https://api.darksky.net/forecast/%s/%s,%s' % (key, latitude, longitude), params={'units': units})
        return r.json()

    def get_results(self, address):
        results = {}
        geocode = self.get_geocode(address)
        if isinstance(geocode, str):
            results['error'] = geocode
        else:
            results['geocode'] = geocode
            results['weather'] = self.get_weather(geocode)
        return results
