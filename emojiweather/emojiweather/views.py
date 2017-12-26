from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import HomeSearchWeatherForm


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicons/default.ico')
    permanent = True


class HomeView(FormMixin, TemplateView):
    form_class = HomeSearchWeatherForm
    template_name = 'home.html'

    def get_form_kwargs(self):
        kwargs = super(HomeView, self).get_form_kwargs()
        ip = get_real_ip(self.request)
        if ip is not None:
            g = GeoIP2()
            record = g.city(ip)
            city = record['city'] if record['city'] else ''
            country = record['country_name'] if record['country_name'] else ''
            delimeter = ', ' if city and country else ''
            kwargs['q'] = '%s%s%s' % (city, delimeter, country)
        return kwargs


class NotFoundView(TemplateView):
    template_name = '404.html'


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
