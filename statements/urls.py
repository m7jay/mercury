from django.urls import path
from .views import StatementsDetailView

urlpatterns = [
    path('', StatementsDetailView.as_view(), name="statements-detail")
]
