from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.edit import FormView

from twilio.twiml.messaging_response import MessagingResponse

from emojiweather.mixins import CsrfExemptMixin
from .forms import EmojiWeatherForm


class SmsView(CsrfExemptMixin, FormView):
    template_name = 'sms/sms.html'
    form_class = EmojiWeatherForm

    def form_valid(self, form):
        # https://www.twilio.com/docs/api/twiml/sms/twilio_request
        address = form.cleaned_data['Body']
        context = {'results': form.get_results(address)}
        message = render_to_string('sms/sms.xml', context)
        response = MessagingResponse()
        response.message(message)
        return HttpResponse(response, content_type='text/xml')
