from django import forms

from emojiweather.mixins import WeatherFormMixin
from search.forms import SearchWeatherForm


class HomeSearchWeatherForm(WeatherFormMixin, SearchWeatherForm, forms.Form):

    def __init__(self, *args, **kwargs):
        q = kwargs.pop('q', None)
        super(HomeSearchWeatherForm, self).__init__(*args, **kwargs)
        self.fields['q'].initial = q
