from django.views.generic.edit import FormView

from .forms import SearchWeatherForm


class SearchView(FormView):
    form_class = SearchWeatherForm
    template_name = 'search/search.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET' and self.request.GET:
            kwargs.update({'data': self.request.GET})
        return kwargs

    def form_valid(self, form):
        self.extra_context = {
            'query': form.cleaned_data['q'],
            'results': form.get_results()
        }
        return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_bound:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().get(request, *args, **kwargs)
