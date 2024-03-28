from django.urls import path
from .views import BalanceSummaryView, TagsSummaryView

urlpatterns = [
    path("balance", BalanceSummaryView.as_view(), name="balance-summary"),
    path("tags", TagsSummaryView.as_view(), name="tags-summary"),
]
