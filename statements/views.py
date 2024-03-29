import io
from logging import getLogger
from typing import Any
from django.views.generic import DetailView, ListView, FormView
import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from statements.services.csv_extract import get_transactions_from_csv
from statements.services.transactions import (
    create_or_update_transactions,
)
from statements.models import Statement, Transaction
from statements.form import UploadFileForm
from statements.serializers import StatementSerializer, TransactionsSerializer

logger = getLogger("__name__")


class StatementsDetailView(DetailView):

    def get(self, request: HttpRequest, unique_id: uuid.UUID) -> HttpResponse:
        logger.info("getting details for statement id: {}".format(str(unique_id)))
        statement: Statement = Statement.objects.get(
            user=request.user, unique_id=unique_id
        )
        transactions = statement.transactions.all().order_by("transaction_date")

        first_transaction: Transaction = transactions.first()
        last_transaction: Transaction = transactions.last()
        # revert the first transaction to get the opening balance
        opening_balance = (
            first_transaction.balance
            + first_transaction.amount_withdrawn
            - first_transaction.amount_deposited
        )
        closing_balance = last_transaction.balance

        return render(
            request,
            "transactions.html",
            {
                "transactions": TransactionsSerializer(transactions, many=True).data,
                "closing_balance": round(closing_balance, 2),
                "opening_balance": round(opening_balance, 2),
            },
        )


class StatementsListView(ListView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        statements = Statement.objects.filter(user=request.user).order_by("month")
        data = StatementSerializer(statements, many=True).data
        for s in data:
            s["diff"] = round(s["closing_balance"] - s["opening_balance"], 2)
        return render(
            request,
            "statements.html",
            {"statements": data},
        )


class UploadFileView(FormView):
    form_class = UploadFileForm
    template_name = "upload.html"

    def post(self, request):
        if request.user.is_authenticated:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data["file"]
                decoded_file = file.read().decode("utf-8")
                io_string = io.StringIO(decoded_file)
                transactions = get_transactions_from_csv(io_string)

                statements = create_or_update_transactions(
                    name=form.cleaned_data["title"],
                    transactions=transactions,
                    user=request.user,
                )
                data = StatementSerializer(statements, many=True)
                for s in data:
                    s["diff"] = round(s["closing_balance"] - s["opening_balance"], 2)

                return render(
                    request,
                    "statements.html",
                    {"statements": data},
                )
            else:
                return self.form_invalid(form)
        else:
            return redirect("/")
