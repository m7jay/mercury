from django.urls import path
from .views import BalanceSummaryView

urlpatterns = [
    path("balance", BalanceSummaryView.as_view(), name="balance-summary"),
]
