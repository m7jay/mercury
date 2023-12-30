from django.views.generic import DetailView
from django.http import JsonResponse

class StatementsDetailView(DetailView):
    def get(self, request):
        response = {"status": "success", "data": "Statements Details View"}
        return JsonResponse(response)