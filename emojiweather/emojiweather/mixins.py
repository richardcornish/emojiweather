from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import geoip2.database
import requests
from ipware.ip import get_real_ip


class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)


class FormKwargsMixin(object):
    def get_form_kwargs(self):
        kwargs = super(FormKwargsMixin, self).get_form_kwargs()
        ip = get_real_ip(self.request)
        if ip is not None:
            reader = geoip2.database.Reader(settings.GEOLITE2_CITY_DB)
            response = reader.city(ip)
            kwargs['q'] = '%s, %s' % (response.city.name, response.subdivisions.most_specific.name)
        return kwargs


class WeatherFormMixin(object):

    def get_geocode(self, address):
        errors = {
            'zero_results': 'We\u2019re sorry, but we could not find %s.' % address,
            'over_query_limit': 'We\u2019re sorry, but the request quota has been reached.',
            'request_denied': 'We\u2019re sorry, but the request was denied.',
            'invalid_request': 'We\u2019re sorry, but the request was invalid.',
            'unknown': 'We\u2019re sorry, but an error occurred.',
        }
        key = settings.GOOGLE_GEOCODING_API_KEY
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={'address': address, 'key': key})
        j = r.json()
        if j['status'] == 'OK':
            return j['results'][0]
        else:
            try:
                return errors[j['status'].lower()]
            except KeyError:
                return errors['unknown']

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
