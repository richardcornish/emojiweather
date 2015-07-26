from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import ContextMixin, TemplateResponseMixin

import twilio.twiml

from .mixins import CsrfExemptMixin


class HomeView(CsrfExemptMixin, ContextMixin, TemplateResponseMixin, View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        response = twilio.twiml.Response()
        response.say('Now joining conference.', voice='woman')
        response.dial().conference('MyRoom')
        return HttpResponse(response, content_type='text/xml')
