from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)
