# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View, TemplateView

import forecastio
import requests
import twilio.twiml

from .mixins import CsrfExemptMixin


class ConferenceView(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        response = twilio.twiml.Response()
        response.say('Now joining conference.', voice='woman')
        response.dial().conference('MyRoom')
        return HttpResponse(response, content_type='text/xml')


class WeatherView(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        body = request.POST.get('Body', None)

        r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s' % body)
        location = r.json()['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']

        try:
            forecast = forecastio.load_forecast(settings.FORECASTIO_API_KEY, latitude, longitude)
            currently = forecast.currently()
            daily = forecast.daily()
            weather = {
                'summary': currently.summary,
                'temperature': str(int(currently.temperature)),
                'moon': daily.data[0].moonPhase * 100,
                'emoji': ''
            }

            if 0 <= weather['moon'] < 6.25 or 93.75 <= weather['moon'] <= 100:
                weather['emoji'] = u'🌑'
            if 6.25 <= weather['moon'] < 18.75:
                weather['emoji'] = u'🌒'
            if 18.75 <= weather['moon'] < 31.25:
                weather['emoji'] = u'🌓'
            if 31.25 <= weather['moon'] < 43.75:
                weather['emoji'] = u'🌔'
            if 43.75 <= weather['moon'] < 56.25:
                weather['emoji'] = u'🌕'
            if 56.25 <= weather['moon'] < 68.75:
                weather['emoji'] = u'🌖'
            if 68.75 <= weather['moon'] < 81.25:
                weather['emoji'] = u'🌗'
            if 81.25 <= weather['moon'] < 93.75:
                weather['emoji'] = u'🌘'

        except Exception as e:
            print e

        response = twilio.twiml.Response()
        # response.media('')
        response.message(u'Weather for %s: %s and %s°F. Moon tonight: %s.' % (body, weather.get('summary'), weather.get('temperature'), weather.get('emoji')))
        return HttpResponse(response, content_type='text/xml')


class HomeView(TemplateView):
    template_name = 'home.html'
