from django.views.generic.edit import FormView

from .forms import SearchWeatherForm


class SearchView(FormView):
    form_class = SearchWeatherForm
    template_name = 'search/search.html'
    query_field = 'q'
    query = None
    results = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({'data': self.request.GET})
        return kwargs

    def form_valid(self, form):
        self.query = form.cleaned_data[self.query_field]
        self.results = form.get_results(self.query)
        return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_bound:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['query'] = self.query
        kwargs['results'] = self.results
        return super().get_context_data(**kwargs)
