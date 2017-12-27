from search.forms import SearchWeatherForm


class HomeSearchWeatherForm(SearchWeatherForm):

    def __init__(self, *args, **kwargs):
        q = kwargs.pop('q', None)
        super(HomeSearchWeatherForm, self).__init__(*args, **kwargs)
        self.fields['q'].initial = q
