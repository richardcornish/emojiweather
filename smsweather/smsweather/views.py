from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from django.views.generic import View, TemplateView, RedirectView

import forecastio
import requests
import twilio.twiml

from .mixins import CsrfExemptMixin
from .icons import conditions, moons


class SmsView(CsrfExemptMixin, View):

    def get_icon(self, slug):
        try:
            return conditions[slug]
        except KeyError:
            return ''

    def get_moon(self, moon_phase):
        moon_phase *= 100
        if 0 <= moon_phase < 6.25 or 93.75 <= moon_phase <= 100:
            return moons[1]
        elif 6.25 <= moon_phase < 18.75:
            return moons[2]
        elif 18.75 <= moon_phase < 31.25:
            return moons[3]
        elif 31.25 <= moon_phase < 43.75:
            return moons[4]
        elif 43.75 <= moon_phase < 56.25:
            return moons[5]
        elif 56.25 <= moon_phase < 68.75:
            return moons[6]
        elif 68.75 <= moon_phase < 81.25:
            return moons[7]
        elif 81.25 <= moon_phase < 93.75:
            return moons[8]
        else:
            return moons[0]

    def post(self, request, *args, **kwargs):
        body = request.POST.get('Body', None)

        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={'address': '%s' % body})
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
                'icon': self.get_icon(currently.icon),
                'summary': currently.summary,
                'temperature': str(int(currently.temperature)),
                'moon': self.get_moon(daily.data[0].moonPhase),
            }
            response.message('%s %s and %s°. %s %s. %s' % (
                weather.get('icon'),
                weather.get('summary'),
                weather.get('temperature'),
                weather.get('moon').get('emoji'),
                weather.get('moon').get('phase'),
                formatted_address
            ))

        except Exception as e:
            response.message('We\'re sorry, but an error occurred: %s' % e)

        return HttpResponse(response, content_type='text/xml')


class HomeView(TemplateView):
    template_name = 'home.html'


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicon.ico')
    permanent = True
