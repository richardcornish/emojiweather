from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from .forms import SearchWeatherForm


class SearchView(FormMixin, TemplateView):
    form_class = SearchWeatherForm
    template_name = 'search/search.html'
    query_field = 'q'
    query = None
    results = None

    def get_form_kwargs(self):
        kwargs = super(SearchView, self).get_form_kwargs()
        if self.request.method in ('GET'):
            if self.query_field in self.request.GET and self.request.GET[self.query_field]:
                kwargs['data'] = self.request.GET
        return kwargs

    def form_valid(self, form):
        self.query = form.cleaned_data[self.query_field]
        self.results = form.get_results(self.query)
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return super(SearchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['query'] = self.query
        kwargs['results'] = self.results
        return super(SearchView, self).get_context_data(**kwargs)
