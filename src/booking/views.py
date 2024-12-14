from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView


class Index(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)


class Home(LoginRequiredMixin, TemplateView):
    pass
