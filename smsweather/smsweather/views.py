from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from .mixins import CsrfExemptMixin

from .forms import SmsWeatherForm, VoiceWeatherForm


class VoiceView(CsrfExemptMixin, FormView):
    form_class = VoiceWeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def form_valid(self, form):
        voice = 'alice'
        language = 'en-GB'
        response = VoiceResponse()
        if form.cleaned_data['SpeechResult']:
            address = form.cleaned_data['SpeechResult']
            weather = form.get_weather(address)
            try:
                message = 'The weather for %s is %s degrees and %s.' % (
                    weather['location']['formatted_address'],
                    weather['temperature'],
                    weather['summary'].lower(),
                )
            except KeyError:
                message = weather['location']['error']
            response.say(message, voice=voice, language=language)
        else:
            response = VoiceResponse()
            gather = Gather(input='speech')
            gather.say('Please say your location.', voice=voice, language=language)
            response.append(gather)
        return HttpResponse(response, content_type='text/xml')


class SmsView(CsrfExemptMixin, FormView):
    form_class = SmsWeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def form_valid(self, form):
        # https://www.twilio.com/docs/api/twiml/sms/twilio_request
        address = form.cleaned_data['Body']
        weather = form.get_weather(address)
        try:
            message = '%s %s and %s\u00B0. %s %s. %s.' % (
                weather['icon'],
                weather['summary'].lower(),
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
