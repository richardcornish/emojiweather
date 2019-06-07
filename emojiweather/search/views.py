from django.views.generic.edit import FormView

from .forms import SearchWeatherForm


class SearchView(FormView):
    form_class = SearchWeatherForm
    template_name = 'search/search.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET' and self.request.GET:
            kwargs['data'] = self.request.GET
        return kwargs

    def form_valid(self, form):
        query = form.cleaned_data['q']
        kwargs = {
            'query': query,
            'results': form.get_results(query),
        }
        return self.render_to_response(self.get_context_data(**kwargs))

    def get(self, request, *args, **kwargs):
        if request.GET:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().get(request, *args, **kwargs)
