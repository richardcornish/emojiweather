from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormMixin

from search.forms import SearchWeatherForm


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicons/default.ico')
    permanent = True


class HomeView(FormMixin, TemplateView):
    form_class = SearchWeatherForm
    template_name = 'home.html'


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
