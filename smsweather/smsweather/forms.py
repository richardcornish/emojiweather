from django import forms
from django.conf import settings

import forecastio
import requests


class WeatherForm(forms.Form):

    def get_location(self, address):
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={'address': address})
        json = r.json()
        if json['status'] == 'OK':
            return {
                'formatted_address': json['results'][0]['formatted_address'],
                'latitude': json['results'][0]['geometry']['location']['lat'],
                'longitude': json['results'][0]['geometry']['location']['lng'],
            }
        else:
            errors = {
                'zero_results': 'We\u2019re sorry, but we could not find that address.',
                'over_query_limit': 'We\u2019re sorry, but the request quota has been reached.',
                'request_denied': 'We\u2019re sorry, but your request was denied.',
                'invalid_request': 'We\u2019re sorry, but we could not find that address.',
                'unknown_error': 'We\u2019re sorry, but an error occurred.',
            }
            try:
                error = errors[json['status'].lower()]
            except KeyError:
                error = errors['unknown_error']
            return {
                'error': '%s %s %s' % ('Beep boop.', error, '\U0001F916'),
            }

    def get_forecast(self, location):
        latitude = location['latitude']
        longitude = location['longitude']
        forecast = forecastio.load_forecast(settings.DARKSKY_API_KEY, latitude, longitude)
        return {
            'currently': forecast.currently(),
            'daily': forecast.daily(),
        }

    def get_icon(self, forecast):
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
            'unknown': '¯\_(ツ)_/¯',
        }
        try:
            return icons[forecast['currently'].icon]
        except KeyError:
            return icons['unknown']

    def get_summary(self, forecast):
        return forecast['currently'].summary

    def get_temperature(self, forecast):
        return str(int(forecast['currently'].temperature))

    def get_moon(self, forecast):
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
        percentage = forecast['daily'].data[0].moonPhase * 100
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

    def get_weather(self, address):
        location = self.get_location(address)
        weather = {
            'location': location,
        }
        if 'latitude' and 'longitude' in location:
            forecast = self.get_forecast(location)
            weather['icon'] = self.get_icon(forecast)
            weather['summary'] = self.get_summary(forecast)
            weather['temperature'] = self.get_temperature(forecast)
            weather['moon'] = self.get_moon(forecast)
        return weather


class SmsWeatherForm(WeatherForm)
    Body = forms.CharField()


class VoiceWeatherForm(WeatherForm)
    SpeechResult = forms.CharField(required=False)
