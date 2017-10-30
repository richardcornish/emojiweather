from django import forms

from smsweather.mixins import WeatherMixin


class SearchWeatherForm(WeatherMixin, forms.Form):
    q = forms.CharField(label='Query', widget=forms.TextInput(attrs={
        'type': 'search',
        'autocorrect': 'off',
        'autofocus': True,
        'class': 'form-control input-lg',
        'placeholder': 'Search for a location',
    }))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SearchWeatherForm, self).__init__(*args, **kwargs)
        if self.request and 'q' in self.request.GET:
            copy = self.request.GET.copy()
            self.fields['q'].initial = copy['q'].strip()
