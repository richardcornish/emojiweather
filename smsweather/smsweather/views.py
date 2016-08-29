from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from django.views.generic import RedirectView, TemplateView, View

import forecastio
import requests
import twilio.twiml

from .icons import icons, phases
from .mixins import CsrfExemptMixin


class SmsView(CsrfExemptMixin, View):

    def get_icon(self, slug):
        try:
            return icons[slug]
        except KeyError:
            return ''

    def get_moon(self, precentage):
        precentage *= 100
        if 0 <= precentage < 6.25 or 93.75 <= precentage <= 100:
            return phases['new-moon']
        elif 6.25 <= precentage < 18.75:
            return phases['waxing-crescent']
        elif 18.75 <= precentage < 31.25:
            return phases['first-quarter']
        elif 31.25 <= precentage < 43.75:
            return phases['waxing-gibbous']
        elif 43.75 <= precentage < 56.25:
            return phases['full-moon']
        elif 56.25 <= precentage < 68.75:
            return phases['waning-gibbous']
        elif 68.75 <= precentage < 81.25:
            return phases['last-quarter']
        elif 81.25 <= precentage < 93.75:
            return phases['waning-crescent']
        else:
            return phases['unknown']

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
                weather.get('moon').get('icon'),
                weather.get('moon').get('name'),
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
