from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy

from .forms import SearchWeatherForm


class SearchView(FormMixin, TemplateView):
    form_class = SearchWeatherForm
    template_name = 'search/search.html'
    query = None
    results = None

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        if 'query' not in kwargs:
            kwargs['query'] = self.query
        if 'results' not in kwargs:
            kwargs['results'] = self.results
        return super(SearchView, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(SearchView, self).get_form_kwargs()
        if self.request.method in ('GET'):
            if 'q' in self.request.GET and self.request.GET['q'] is not None:
                kwargs.update({
                    'data': self.request.GET,
                })
        return kwargs

    def form_valid(self, form):
        self.query = form.cleaned_data['q']
        self.results = form.get_results(self.query)
        return self.render_to_response(self.get_context_data(form=form))
