from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.syndication.views import add_domain
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.views.generic.edit import FormView

from emojiweather.mixins import CsrfExemptMixin
from .forms import ChatForm


class ChatView(CsrfExemptMixin, FormView):
    form_class = ChatForm
    template_name = 'chat/chat.html'

    def get(self, *args, **kwargs):
        return HttpResponseForbidden()

    def form_invalid(self, form):
        return HttpResponseForbidden()

    def get_icon_url(self, name):
        current_site = get_current_site(self.request)
        url = staticfiles_storage.url(name)
        return add_domain(current_site.domain, url, self.request.is_secure())

    def form_valid(self, form):
        # https://developers.mattermost.com/integrate/slash-commands/
        token = form.cleaned_data['token']
        if token == settings.MATTERMOST_TOKEN:
            if form.cleaned_data['command'][1:] == 'hot':
                data = {
                    'text': render_to_string('chat/chat.md', form.cleaned_data),
                    'response_type': 'in_channel',
                    'username': 'csibot',
                    'icon_url': self.get_icon_url('img/chat-icon.png'),
                }
                return JsonResponse(data)
        return HttpResponseForbidden()
