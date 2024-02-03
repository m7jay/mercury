from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.views.generic import DetailView

from statements.models import Transaction


class BalanceSummaryView(DetailView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        transactions = Transaction.objects.filter(
            statement__user=request.user
        ).order_by("transaction_date")
        data = {}
        for transaction in transactions:
            if transaction.transaction_date not in data:
                data[transaction.transaction_date] = transaction.balance

        labels, values = zip(*data.items())

        context = {
            "labels": labels,
            "values": values,
        }
        return render(
            request,
            "balace_summary.html",
            context,
        )
