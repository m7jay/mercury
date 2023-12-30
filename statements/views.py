from django.views.generic import DetailView
from django.http import JsonResponse
from django.shortcuts import render

class StatementsDetailView(DetailView):
    def get(self, request):
        return render(request, "index.html")