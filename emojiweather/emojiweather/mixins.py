from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import requests


class CsrfExemptMixin:

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class WeatherFormMixin:

    def _geocode(self, data):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        key = settings.GOOGLE_GEOCODING_API_KEY
        r = requests.get(url, params={'address': data, 'key': key})
        data = {}
        if r.status_code == 200:
            j = r.json()
            if j['status'] == 'OK':
                data.update({
                    'status': j['status'],
                    'results': j['results'][0]
                })
            else:
                errors = {
                    'ZERO_RESULTS': 'No results were found.',
                    'OVER_DAILY_LIMIT': 'The daily limit has been reached.',
                    'OVER_QUERY_LIMIT': 'The request quota has been reached.',
                    'REQUEST_DENIED': 'The request was denied.',
                    'INVALID_REQUEST': 'The request was invalid.',
                    'UNKNOWN_ERROR': 'An error occurred.',
                }
                data.update({
                    'status': errors.get(j['status'], errors['UNKNOWN_ERROR']),
                    'results': None
                })
        return data

    def _get_weather(self, data):
        key = settings.DARK_SKY_API_KEY
        latitude = data['results']['geometry']['location']['lat']
        longitude = data['results']['geometry']['location']['lng']
        units = 'auto'
        url = f'https://api.darksky.net/forecast/{key}/{latitude},{longitude}'
        r = requests.get(url, params={'units': units})
        data = {}
        if r.status_code == 200:
            j = r.json()
            if j.get('code') and j['code'] == '400':
                data.update({
                    'status': j['error'],
                    'results': None,
                })
            else:
                data.update({
                    'status': 'OK',
                    'results': j,
                })
        return data

    def _get_temperature(self, data):
        temp = data['results']['currently']['temperature']
        units = data['results']['flags']['units']
        data = {}
        if units == 'us':
            data.update({
                'f': temp,
                'c': (temp - 32) * 5 / 9,
            })
        else:
            data.update({
                'f': (temp * 9 / 5) + 32,
                'c': temp,
            })
        return data

    def get_results(self):
        address = self.cleaned_data['q']
        data = {
            'geocode': self._geocode(address),
            'weather': None,
            'temperature': None,
        }
        if data['geocode'] and data['geocode']['results'] is not None:
            data.update({'weather': self._get_weather(data['geocode'])})
        if data['weather'] and data['weather']['results'] is not None:
            data.update({'temperature': self._get_temperature(data['weather'])})
        return data
