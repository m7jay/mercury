from django.urls import path
from .views import StatementsDetailView

urlpatterns = [
    path('details', StatementsDetailView.as_view(), name="statements-detail")
]
