from django import forms

from emojiweather.mixins import WeatherMixin


class EmojiWeatherForm(WeatherMixin, forms.Form):
    Body = forms.CharField()
