from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View, TemplateView

import forecastio
import requests
import twilio.twiml

from .mixins import CsrfExemptMixin


class SmsView(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        body = request.POST.get('Body', None)

        r = requests.get('http://maps.googleapis.com/maps/api/geocode/json', params={'address': '%s'} % body)
        location = r.json()['results'][0]['geometry']['location']
        formatted_address = r.json()['results'][0]['formatted_address']
        latitude = location['lat']
        longitude = location['lng']

        response = twilio.twiml.Response()
        try:
            forecast = forecastio.load_forecast(settings.FORECASTIO_API_KEY, latitude, longitude)
            currently = forecast.currently()
            daily = forecast.daily()
            weather = {
                'summary': currently.summary,
                'temperature': str(int(currently.temperature)),
                'moon': daily.data[0].moonPhase * 100,
                'moon_emoji': ''
            }

            if 0 <= weather['moon'] < 6.25 or 93.75 <= weather['moon'] <= 100:
                weather['moon_emoji'] = '🌑'
            elif 6.25 <= weather['moon'] < 18.75:
                weather['moon_emoji'] = '🌒'
            elif 18.75 <= weather['moon'] < 31.25:
                weather['moon_emoji'] = '🌓'
            elif 31.25 <= weather['moon'] < 43.75:
                weather['moon_emoji'] = '🌔'
            elif 43.75 <= weather['moon'] < 56.25:
                weather['moon_emoji'] = '\U0001F315'
            elif 56.25 <= weather['moon'] < 68.75:
                weather['moon_emoji'] = '🌖'
            elif 68.75 <= weather['moon'] < 81.25:
                weather['moon_emoji'] = '🌗'
            elif 81.25 <= weather['moon'] < 93.75:
                weather['moon_emoji'] = '🌘'
            else:
                weather['moon_emoji'] = 'Unknown'

            response.message('Weather for %s: %s and %s°F. Moon tonight: %s.' % (formatted_address, weather.get('summary'), weather.get('temperature'), weather.get('moon_emoji')))

        except Exception as e:
            response.message('We\'re sorry, but an error occurred: %s' % e)

        return HttpResponse(response, content_type='text/xml')


class HomeView(TemplateView):
    template_name = 'home.html'
