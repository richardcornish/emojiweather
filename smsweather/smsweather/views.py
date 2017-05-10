from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from django.views.generic import RedirectView, TemplateView, View

import forecastio
import requests
from twilio import twiml

from .icons import icons, phases
from .mixins import CsrfExemptMixin


class SmsView(CsrfExemptMixin, View):

    errors = {
        'zero_results': "Beep boop. We're sorry, but we could not find that address. \U0001F916",
        'over_query_limit': "Beep boop. We're sorry, but the request quota has been reached. \U0001F916",
        'request_denied': "Beep boop. We're sorry, but your request was denied. \U0001F916",
        'invalid_request': "Beep boop. We're sorry, but we could not find that address. \U0001F916",
        'unknown_error': "Beep boop. We're sorry, but an error occurred. \U0001F916",
    }

    def get_moon(self, percentage):
        percentage *= 100
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

    def post(self, request, *args, **kwargs):
        body = request.POST.get('Body', None)
        response = twiml.Response()
        try:

            # Get geocoded location
            r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={'address': body})
            json = r.json()

            if json['status'] == 'OK':

                # Get coordinates
                formatted_address = json['results'][0]['formatted_address']
                location = json['results'][0]['geometry']['location']
                latitude = location['lat']
                longitude = location['lng']

                # Get weather forecast
                forecast = forecastio.load_forecast(settings.DARKSKY_API_KEY, latitude, longitude)
                currently = forecast.currently()
                daily = forecast.daily()
                weather = {
                    'icon': icons.get(currently.icon, ''),
                    'summary': currently.summary,
                    'temperature': str(int(currently.temperature)),
                    'moon': self.get_moon(daily.data[0].moonPhase),
                }

                # Create Twilio response
                response.message('%s %s and %s°. %s %s. %s.' % (
                    weather.get('icon'),
                    weather.get('summary'),
                    weather.get('temperature'),
                    weather.get('moon').get('icon'),
                    weather.get('moon').get('name'),
                    formatted_address
                ))

            else:
                try:
                    response.message(self.errors[json['status'].lower()])
                except IndexError:
                    response.message(self.errors['unknown_error'])

        except Exception as error:
            response.message('%s %s' % (self.errors['unknown_error'], error))
        return HttpResponse(response, content_type='text/xml')


class HomeView(TemplateView):
    template_name = 'home.html'


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicon.ico')
    permanent = True
