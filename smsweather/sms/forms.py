from django import forms

from smsweather.mixins import WeatherMixin


class SmsWeatherForm(WeatherMixin, forms.Form):
    Body = forms.CharField()
