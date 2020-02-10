from django.http import HttpResponse
from django.views.generic import View

from emojiweather.mixins import CsrfExemptMixin


class WhatsAppView(CsrfExemptMixin, View):

    def get(self, *args, **kwargs):
        return HttpResponse()

    def post(self, *args, **kwargs):
        return HttpResponse()
