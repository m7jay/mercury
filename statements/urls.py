from django.urls import path
from .views import StatementsDetailView, TransactionsListView

urlpatterns = [
    path('', StatementsDetailView.as_view(), name="statements-detail"),
    path('transactions', TransactionsListView.as_view(), name="transactions")
]
