from logging import getLogger
from django.views.generic import DetailView
from django.shortcuts import render
from django.shortcuts import render, redirect

logger = getLogger("__name__")


class LandingPage(DetailView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/statements/")
        return render(request, "index.html")
