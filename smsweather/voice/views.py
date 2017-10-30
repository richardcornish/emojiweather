from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.edit import FormView

from twilio.twiml.voice_response import Gather, VoiceResponse

from smsweather.mixins import CsrfExemptMixin
from .forms import VoiceWeatherForm


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
        context = {'results': form.get_results(address)}
        message = render_to_string('voice/voice.xml', context)
        response = VoiceResponse()
        gather = Gather(input='dtmf speech', timeout=2, numDigits=5)
        gather.say(message, voice='alice')
        response.append(gather)
        response.redirect(reverse('voice'))
        return HttpResponse(response, content_type='text/xml')
