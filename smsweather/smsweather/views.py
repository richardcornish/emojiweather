from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


# class FaviconView(RedirectView):
#     url = staticfiles_storage.url('img/favicon.ico')
#     permanent = True
