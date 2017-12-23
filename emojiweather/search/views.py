from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

from emojiweather.mixins import FormKwargsMixin
from .forms import SearchWeatherForm


class SearchView(FormKwargsMixin, FormMixin, TemplateView):
    form_class = SearchWeatherForm
    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):
        query = None
        results = None
        if 'q' in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                query = form.cleaned_data['q']
                results = form.get_results(query)
        else:
            form = self.get_form()
        context = self.get_context_data(form=form, query=query, results=results)
        return self.render_to_response(context)
