from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import HomeSearchWeatherForm
from utils import get_location_from_ip


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicons/default.ico')
    permanent = False


class HomeView(FormMixin, TemplateView):
    form_class = HomeSearchWeatherForm
    template_name = 'home.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['q'] = get_location_from_ip(self.request)
        return kwargs


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
