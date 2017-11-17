from django import forms

from smsweather.mixins import WeatherMixin


class SearchWeatherForm(WeatherMixin, forms.Form):
    q = forms.CharField(label='Query', widget=forms.TextInput(attrs={
        'type': 'search',
        'autocapitalize': 'words',
        'autocorrect': 'off',
        'autofocus': True,
        'class': 'form-control form-control-lg text-center',
        'placeholder': 'Search for a location',
    }))
