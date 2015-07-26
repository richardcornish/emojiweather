from django.views.generic import View
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.template.loader import render_to_string

import twilio.twiml


class HomeView(ContextMixin, TemplateResponseMixin, View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        response = twilio.twiml.Response()
        response.say("Hello Monkey")
        return render_to_string(response)
