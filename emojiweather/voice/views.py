from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.edit import FormView

from twilio.twiml.voice_response import Gather, VoiceResponse

from emojiweather.mixins import CsrfExemptMixin
from .forms import VoiceWeatherForm


class VoiceView(CsrfExemptMixin, FormView):
    template_name = 'voice/voice.html'
    form_class = VoiceWeatherForm

    def form_valid(self, form):
        # https://www.twilio.com/docs/api/twiml/gather
        if form.cleaned_data['SpeechResult']:
            query = form.cleaned_data['SpeechResult']
        elif form.cleaned_data['Digits']:
            query = form.cleaned_data['Digits']
        else:
            query = None
        results = form.get_results(query) if query else None
        context = {'results': results}
        message = render_to_string('voice/voice.xml', context)
        response = VoiceResponse()
        gather = Gather(input='dtmf speech', timeout=2, numDigits=5)
        gather.say(message, voice='alice')
        response.append(gather)
        response.redirect(reverse('voice'))
        return HttpResponse(response, content_type='text/xml')
