from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.views.generic import DetailView

from statements.models import Transaction, Statement
from statements.serializers import StatementSerializer, TransactionsSerializer


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


class TagsSummaryView(DetailView):
    EXPENSES_TAGS = [
        "google",
        "jio",
        "amazon",
        "swiggy",
        "uber",
        "airtel",
    ]
    INCOME_TAGS = ["salary"]

    def __get_tag_for_transaction(self, transaction: Transaction):
        tags = self.EXPENSES_TAGS if transaction.amount_withdrawn else self.INCOME_TAGS
        for tag in tags:
            if tag in transaction.transaction_id.lower():
                return tag

        return None

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        transactions = Transaction.objects.filter(
            statement__user=request.user
        ).order_by("transaction_date")

        expenses = {}
        incomes = {}

        for txn in transactions:
            txn_month = txn.transaction_date.strftime("%b - %Y")
            tag = self.__get_tag_for_transaction(transaction=txn)
            if txn.amount_withdrawn:
                if tag not in expenses:
                    expenses[tag] = {}
                if txn_month not in expenses[tag]:
                    expenses[tag][txn_month] = txn.amount_withdrawn
                else:
                    expenses[tag][txn_month] += txn.amount_withdrawn
            if txn.amount_deposited:
                if tag not in incomes:
                    incomes[tag] = {}
                if txn_month not in incomes[tag]:
                    incomes[tag][txn_month] = txn.amount_deposited
                else:
                    incomes[tag][txn_month] += txn.amount_deposited
        context = {}
        for tag, monthly_map in expenses.items():
            if tag not in context:
                context[tag] = {}
            context[tag] = {
                "labels": list(monthly_map.keys()),
                "values": list(monthly_map.values()),
            }

        for tag, monthly_map in incomes.items():
            if tag not in context:
                context[tag] = {}
            context[tag] = {
                "labels": list(monthly_map.keys()),
                "values": list(monthly_map.values()),
            }

        return render(
            request,
            "tags-summary.html",
            context,
        )
