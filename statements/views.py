from typing import Any
from django.views.generic import DetailView, ListView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from statements.models import Transaction


class StatementsDetailView(DetailView):
    def get(self, request):
        return render(request, "index.html")


class TransactionsListView(ListView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        transactions = [
            Transaction(
                transaction_id="txn_001",
                transaction_date="2023-12-01",
                amount_deposited="100.00",
                amount_withdrawn=None,
                balance="100.00",
                others="First money",
            ),
            Transaction(
                transaction_id="txn_002",
                transaction_date="2023-12-02",
                amount_deposited="100.00",
                amount_withdrawn=None,
                balance="200.00",
                others="Second money",
            ),
            Transaction(
                transaction_id="txn_003",
                transaction_date="2023-12-03",
                amount_deposited=None,
                amount_withdrawn="50.00",
                balance="150.00",
                others="Third money",
            ),
            Transaction(
                transaction_id="txn_004",
                transaction_date="2023-12-04",
                amount_deposited="100.00",
                amount_withdrawn=None,
                balance="250.00",
                others="Fourht money",
            ),
            Transaction(
                transaction_id="txn_005",
                transaction_date="2023-12-05",
                amount_deposited=None,
                amount_withdrawn="50.00",
                balance="200.00",
                others=None,
            ),
        ]
        return render(request, "transactions.html", {"transactions": transactions})
