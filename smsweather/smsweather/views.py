from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import RedirectView, TemplateView, View
from django.views.generic.edit import FormView

from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from .mixins import CsrfExemptMixin

from .forms import WeatherForm


class VoiceView(CsrfExemptMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        message = 'Thank you for calling.'
        response = VoiceResponse()
        response.say(message, voice='alice', loop='0', language='en-GB')
        response.hangup()
        return HttpResponse(response, content_type='text/xml')


class SmsView(CsrfExemptMixin, FormView):
    form_class = WeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def form_valid(self, form):
        body = form.cleaned_data['Body']
        weather = form.get_weather(body)
        try:
            message = '%s %s and %s°. %s %s. %s.' % (
                weather['icon'],
                weather['summary'],
                weather['temperature'],
                weather['moon']['icon'],
                weather['moon']['name'],
                weather['location']['formatted_address'],
            )
        except KeyError:
            message = weather['location']['error']
        response = MessagingResponse()
        response.message(message)
        return HttpResponse(response, content_type='text/xml')


class HomeView(TemplateView):
    template_name = 'home.html'


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicon.ico')
    permanent = True
