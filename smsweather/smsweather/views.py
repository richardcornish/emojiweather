from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from twilio import twiml
from .mixins import CsrfExemptMixin

from .forms import WeatherForm


class SmsView(CsrfExemptMixin, FormView):
    form_class = WeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponse()

    def form_valid(self, form):
        body = form.cleaned_data['Body']
        weather = form.get_weather(body)
        response = twiml.Response()
        try:
            message = '%s %s and %s°. %s %s. %s.' % (
                weather['icon'],
                weather['summary'],
                weather['temperature'],
                weather['moon']['icon'],
                weather['moon']['name'],
                weather['location']['formatted_address'],
            )
        except IndexError:
            message = weather['location']['error']
        response.message(form.cleaned_data)
        return HttpResponse(response, content_type='text/xml')


class HomeView(TemplateView):
    template_name = 'home.html'


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicon.ico')
    permanent = True
