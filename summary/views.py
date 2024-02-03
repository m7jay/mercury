from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.views.generic import DetailView

from statements.models import Transaction, Statement
from statements.serializers import StatementSerializer


class BalanceSummaryView(DetailView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        statements = Statement.objects.filter(user=request.user).order_by("month")
        data = StatementSerializer(statements, many=True).data
        balances = {}
        for statement in data:
            balances[statement["month"]] = statement["closing_balance"]

        transactions = Transaction.objects.filter(
            statement__user=request.user
        ).order_by("transaction_date")
        data = {}
        expenses = {}
        incomes = {}

        for txn in transactions:
            txn_month = txn.transaction_date.strftime("%b - %Y")
            if txn.amount_withdrawn:
                if txn_month not in expenses:
                    expenses[txn_month] = txn.amount_withdrawn
                else:
                    expenses[txn_month] += txn.amount_withdrawn
            if txn.amount_deposited:
                if txn_month not in incomes:
                    incomes[txn_month] = txn.amount_deposited
                else:
                    incomes[txn_month] += txn.amount_deposited

        context = {
            "balances": {
                "labels": list(balances.keys()),
                "values": list(balances.values()),
            },
            "expenses": {
                "labels": list(expenses.keys()),
                "values": list(expenses.values()),
            },
            "incomes": {
                "labels": list(incomes.keys()),
                "values": list(incomes.values()),
            },
        }
        return render(
            request,
            "summary.html",
            context,
        )
