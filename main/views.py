from logging import getLogger
from django.views.generic import DetailView
from django.shortcuts import render

logger = getLogger("__name__")


class LandingPage(DetailView):
    def get(self, request):
        return render(request, "index.html")
