from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormMixin

from ipware.ip import get_real_ip

from .forms import HomeSearchWeatherForm


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicons/default.ico')
    permanent = False


class HomeView(FormMixin, TemplateView):
    form_class = HomeSearchWeatherForm
    template_name = 'home.html'

    def get_form_kwargs(self):
        kwargs = super(HomeView, self).get_form_kwargs()
        ip = get_real_ip(self.request)
        if ip:
            g = GeoIP2()
            record = g.city(ip)
            if record:
                city = record['city'] if 'city' in record and record['city'] else ''
                country = record['country_name'] if 'country_name' in record and record['country_name'] else ''
                delimeter = ', ' if city and country else ''
                kwargs['q'] = '%s%s%s' % (city, delimeter, country)
        return kwargs


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
