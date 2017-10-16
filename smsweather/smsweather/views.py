from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse

from .forms import SmsWeatherForm, VoiceWeatherForm
from .mixins import CsrfExemptMixin


class VoiceView(CsrfExemptMixin, FormView):
    form_class = VoiceWeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def form_valid(self, form):
        if form.cleaned_data['SpeechResult']:
            address = form.cleaned_data['SpeechResult']
        elif form.cleaned_data['Digits']:
            address = form.cleaned_data['Digits']
        else:
            address = '%s %s %s %s' % (
                form.cleaned_data['FromCity'],
                form.cleaned_data['FromState'],
                form.cleaned_data['FromZip'],
                form.cleaned_data['FromCountry'],
            )
            address = address.strip()
        context = form.get_weather(address)
        message = render_to_string('voice.txt', context)
        response = VoiceResponse()
        gather = Gather(input='dtmf speech', timeout=2, numDigits=5)
        gather.say(message, voice='alice')
        response.append(gather)
        response.redirect(reverse('voice'))
        return HttpResponse(response, content_type='text/xml')


class SmsView(CsrfExemptMixin, FormView):
    form_class = SmsWeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def form_valid(self, form):
        # https://www.twilio.com/docs/api/twiml/sms/twilio_request
        address = form.cleaned_data['Body']
        context = form.get_weather(address)
        message = render_to_string('sms.txt', context)
        response = MessagingResponse()
        response.message(message)
        return HttpResponse(response, content_type='text/xml')


class HomeView(TemplateView):
    template_name = 'home.html'


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicon.ico')
    permanent = True
