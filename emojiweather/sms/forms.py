from django import forms

from emojiweather.mixins import WeatherFormMixin


class EmojiWeatherForm(WeatherFormMixin, forms.Form):
    Body = forms.CharField()
