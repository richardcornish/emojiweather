from django import forms
from django.conf import settings

from emojiweather.mixins import WeatherFormMixin


class CommandForm(WeatherFormMixin, forms.Form):
    channel_id = forms.CharField(required=False)
    channel_name = forms.CharField(required=False)
    command = forms.CharField(required=False)
    response_url = forms.CharField(required=False)
    team_domain = forms.CharField(required=False)
    team_id = forms.CharField(required=False)
    text = forms.CharField(required=False)
    token = forms.CharField(required=False)
    user_id = forms.CharField(required=False)
    user_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.token_name = kwargs.pop('token_name', None)
        super(CommandForm, self).__init__(*args, **kwargs)

    def clean_token(self):
        token = self.cleaned_data['token']
        if token != getattr(settings, self.token_name, ''):
            raise forms.ValidationError('Invalid token')
        return token
