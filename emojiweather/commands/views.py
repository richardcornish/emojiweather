import random
from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.syndication.views import add_domain
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic.edit import FormView

import pytz
import requests

from .data.ask import MAGIC_8_BALL_RESPONSES
from .data.fact import RANDOM_FACTS
from .data.weather import WEATHER_EMOJI
from .forms import CommandForm
from emojiweather.mixins import CsrfExemptMixin


class BaseCommandView(FormView):
    form_class = CommandForm
    response_class = JsonResponse
    token_name = None
    data = {
        'response_type': 'in_channel',
        'username': 'csibot',
        'icon_url': None,
        'text': None,
    }

    def dispatch(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        path = staticfiles_storage.url('img/chat-icon.png')
        self.data['icon_url'] = add_domain(current_site.domain, path, request.is_secure())
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return HttpResponseForbidden()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['token_name'] = self.token_name
        return kwargs

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data())

    def form_invalid(self, form):
        return HttpResponseForbidden()

    def render_to_response(self, context):
        self.data['text'] = render_to_string(self.template_name, context)
        return self.response_class(self.data)


class AskCommandView(CsrfExemptMixin, BaseCommandView):
    template_name = 'commands/ask.md'
    token_name = 'MATTERMOST_TOKEN_ASK'
    DEFAULT_ERROR = 'Please state your query in the form of a question.'

    def form_valid(self, form):
        if form.cleaned_data['text'] and form.cleaned_data['text'][-1:] == '?':
            response = random.choice(MAGIC_8_BALL_RESPONSES)
        else:
            response = self.DEFAULT_ERROR
        self.extra_context = {
            'user_name': form.cleaned_data['user_name'],
            'text': form.cleaned_data['text'],
            'response': response,
        }
        return super().form_valid(form)


class ChuckCommandView(CsrfExemptMixin, BaseCommandView):
    template_name = 'commands/chuck.md'
    token_name = 'MATTERMOST_TOKEN_CHUCK'

    def form_valid(self, form):
        r = requests.get('http://api.icndb.com/jokes/random')
        if r.status_code != 200 or r.json()['type'] != 'success':
            return HttpResponseForbidden()
        self.extra_context = {'text': r.json()['value']['joke']}
        return super().form_valid(form)


class FactCommandView(CsrfExemptMixin, BaseCommandView):
    template_name = 'commands/fact.md'
    token_name = 'MATTERMOST_TOKEN_FACT'

    def form_valid(self, form):
        self.extra_context = {'text': random.choice(RANDOM_FACTS)}
        return super().form_valid(form)


class HotCommandView(CsrfExemptMixin, BaseCommandView):
    template_name = 'commands/hot.md'
    token_name = 'MATTERMOST_TOKEN_HOT'
    DEFAULT_LENGTH = 1

    def form_valid(self, form):
        try:
            length = int(form.cleaned_data['text'])
        except ValueError:
            length = self.DEFAULT_LENGTH
        self.extra_context = {'list': list(range(length))}
        return super().form_valid(form)


class PrintCommandView(CsrfExemptMixin, BaseCommandView):
    template_name = 'commands/print.md'
    token_name = 'MATTERMOST_TOKEN_PRINT'

    def form_valid(self, form):
        if not form.cleaned_data['text']:
            return HttpResponseForbidden()
        self.extra_context = {'text': form.cleaned_data['text']}
        return super().form_valid(form)


class WeatherCommandView(CsrfExemptMixin, BaseCommandView):
    template_name = 'commands/weather.md'
    token_name = 'MATTERMOST_TOKEN_WEATHER'
    DEFAULT_QUERY = '2100 E Lake Cook Rd, Buffalo Grove, IL 60089'
    DEFAULT_UNKNOWN_EMOJI = ':confused:'

    def form_valid(self, form):
        query = form.cleaned_data['text'] or self.DEFAULT_QUERY
        results = form.get_results(query)
        if 'error' in results:
            return HttpResponseForbidden()
        location = results['geocode']['formatted_address']
        tz = pytz.timezone(results['weather']['timezone'])
        timezone.activate(tz)
        alerts = results['weather'].get('alerts', [])
        for alert in alerts:
            alert.update({
                'time': datetime.fromtimestamp(alert['time'], tz=tz),
                'expires': datetime.fromtimestamp(alert['expires'], tz=tz),
            })
        forecast = []
        for day in results['weather']['daily']['data']:
            forecast.append({
                'date': datetime.fromtimestamp(day['time'], tz=tz),
                'conditions': day['summary'],
                'high': int(day['temperatureHigh']),
                'low': int(day['temperatureLow']),
                'icon': WEATHER_EMOJI.get(day['icon'], self.DEFAULT_UNKNOWN_EMOJI),
            })
        self.extra_context = {
            'alerts': alerts,
            'location': location,
            'forecast': forecast,
        }
        return super().form_valid(form)