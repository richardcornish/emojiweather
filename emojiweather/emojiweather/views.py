from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormMixin

from search.forms import SearchWeatherForm
from utils import get_location_from_ip


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicons/default.ico')
    permanent = False


class HomeView(FormMixin, TemplateView):
    form_class = SearchWeatherForm
    template_name = 'home.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['q'] = get_location_from_ip(self.request)
        return initial


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
