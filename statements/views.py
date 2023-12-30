from typing import Any
from django.views.generic import DetailView, ListView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from statements.pydantic import Transaction
from typing import List
from statements.services.transactions import get_transactions


class StatementsDetailView(DetailView):
    def get(self, request):
        return render(request, "index.html")


class TransactionsListView(ListView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        opening_balance = 371535.33
        closing_balance = opening_balance
        transactions: List[Transaction] = get_transactions(
            file_path="/Users/jayachandram/src/explore/bank-statements/test.pdf",
            password="JAYA1411",
        )
        for transaction in transactions:
            closing_balance = (
                closing_balance
                + (
                    round(float(transaction.amount_deposited), 2)
                    if transaction.amount_deposited
                    else 0.0
                )
                - (
                    round(float(transaction.amount_withdrawn), 2)
                    if transaction.amount_withdrawn
                    else 0.0
                )
            )
        return render(
            request,
            "transactions.html",
            {
                "transactions": [txn.model_dump() for txn in transactions],
                "closing_balance": round(closing_balance, 2),
                "opening_balance": round(opening_balance, 2),
            },
        )
