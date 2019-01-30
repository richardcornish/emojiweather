import random
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.syndication.views import add_domain
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.views.generic.edit import FormView

import requests

from .data.ask import MAGIC_8_BALL_RESPONSES
from .data.fact import RANDOM_FACTS
from .data.weather import WEATHER_ICONS
from .forms import CommandForm
from emojiweather.mixins import CsrfExemptMixin


class AuthenticateTokenMixin(object):

    def form_valid(self, form):
        token = form.cleaned_data['token']
        if token != settings.MATTERMOST_TOKENS.get(self.token_key, ''):
            return HttpResponseForbidden()
        return super(AuthenticateTokenMixin, self).form_valid(form)


class BaseCommandView(FormView):
    form_class = CommandForm
    response_class = JsonResponse
    token_key = ''
    data = {
        'response_type': 'in_channel',
        'username': 'csibot',
        'icon_url': '',
        'text': '',
    }

    def dispatch(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        path = staticfiles_storage.url('img/chat-icon.png')
        self.data['icon_url'] = add_domain(current_site.domain, path, self.request.is_secure())
        return super(BaseCommandView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return HttpResponseForbidden()

    def form_invalid(self, form):
        return HttpResponseForbidden()

    def render_to_response(self, context, **response_kwargs):
        self.data['text'] = render_to_string(self.template_name, context)
        return self.response_class(self.data)


class AskCommandView(CsrfExemptMixin, AuthenticateTokenMixin, BaseCommandView):
    token_key = 'ask'
    template_name = 'commands/ask.md'
    DEFAULT_ERROR = 'Please state your query in the form of a question.'

    def form_valid(self, form):
        if form.cleaned_data['text']:
            if form.cleaned_data['text'][-1:] == '?':
                response = random.choice(MAGIC_8_BALL_RESPONSES)
            else:
                response = self.DEFAULT_ERROR
            kwargs = {'response': response}
            kwargs.update(form.cleaned_data)
            return self.render_to_response(self.get_context_data(**kwargs))
        return HttpResponseForbidden()


class ChuckCommandView(CsrfExemptMixin, AuthenticateTokenMixin, BaseCommandView):
    token_key = 'chuck'
    template_name = 'commands/chuck.md'

    def form_valid(self, form):
        r = requests.get('http://api.icndb.com/jokes/random')
        if r.status_code == 200 and r.json()['type'] == 'success':
            chuck = r.json()['value']['joke']
            return self.render_to_response(self.get_context_data(chuck=chuck))
        return HttpResponseForbidden()


class PrintCommandView(CsrfExemptMixin, AuthenticateTokenMixin, BaseCommandView):
    token_key = 'print'
    template_name = 'commands/print.md'

    def form_valid(self, form):
        if form.cleaned_data['text']:
            p = form.cleaned_data['text']
            return self.render_to_response(self.get_context_data(print=p))
        return HttpResponseForbidden()


class FactCommandView(CsrfExemptMixin, AuthenticateTokenMixin, BaseCommandView):
    token_key = 'fact'
    template_name = 'commands/fact.md'

    def form_valid(self, form):
        fact = random.choice(RANDOM_FACTS)
        return self.render_to_response(self.get_context_data(fact=fact))


class HotCommandView(CsrfExemptMixin, AuthenticateTokenMixin, BaseCommandView):
    token_key = 'hot'
    template_name = 'commands/hot.md'
    DEFAULT_LENGTH = 1

    def form_valid(self, form):
        try:
            length = int(form.cleaned_data['text'])
        except ValueError:
            length = self.DEFAULT_LENGTH
        l = list(range(length))
        return self.render_to_response(self.get_context_data(list=l))


class WeatherCommandView(CsrfExemptMixin, AuthenticateTokenMixin, BaseCommandView):
    token_key = 'weather'
    template_name = 'commands/weather.md'
    DEFAULT_QUERY = '2100 E Lake Cook Rd, Buffalo Grove, IL 60089'

    def form_valid(self, form):
        query = form.cleaned_data['text'] or self.DEFAULT_QUERY
        results = form.get_results(query)
        if 'error' in results:
            context = {'error': results['error']}
        else:
            location = results['geocode']['formatted_address']
            alerts = results['weather'].get('alerts')
            for alert in alerts:
                alert.update({
                    'time': datetime.fromtimestamp(alert['time'], timezone.utc),
                    'expires': datetime.fromtimestamp(alert['expires'], timezone.utc),
                })
            forecast = []
            for day in results['weather']['daily']['data']:
                forecast.append({
                    'date': datetime.fromtimestamp(day['time'], timezone.utc),
                    'summary': day['summary'],
                    'high': int(day['temperatureHigh']),
                    'low': int(day['temperatureLow']),
                    'icon': WEATHER_ICONS.get(day['icon'], ':confused:'),
                })
            context = {
                'alerts': alerts,
                'location': location,
                'forecast': forecast,
            }
        return self.render_to_response(self.get_context_data(**context))
