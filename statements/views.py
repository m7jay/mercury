from typing import Any
from django.views.generic import DetailView, ListView, FormView

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from statements.pydantic import TransactionEntity
from typing import List
from statements.services.transactions import (
    get_transactions,
    get_transactions_from_uploaded_file,
    create_or_update_transactions,
)
from statements.models import Statement
from django.contrib.auth.decorators import login_required
from statements.form import UploadFileForm
from statements.serializers import StatementsSerializer
from datetime import date


class LandingPage(DetailView):
    def get(self, request):
        return render(request, "index.html")


class StatementsDetailView(DetailView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        opening_balance = 371535.33
        closing_balance = opening_balance
        transactions: List[TransactionEntity] = get_transactions(
            file_path="./test.pdf",
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


class StatementsListView(ListView):
    @login_required
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        statements = Statement.objects.filter(user=request.user).order_by("month")
        return render(request, "statements.html", {"statements": statements})


class UploadFileView(FormView):
    form_class = UploadFileForm
    template_name = "upload.html"

    def post(self, request):
        if request.user.is_authenticated:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                # handle file input & create statement, transactions
                transactions = get_transactions_from_uploaded_file(
                    form.cleaned_data["title"],
                    form.cleaned_data["file"],
                    password=form.cleaned_data["password"],
                )
                print(f"{transactions=}")
                statements = create_or_update_transactions(
                    name=form.cleaned_data["title"],
                    transactions=transactions,
                    user=request.user,
                )
                serialized_statements = StatementsSerializer(statements, many=True)
                return render(
                    request,
                    "statements.html",
                    {"statements": serialized_statements.data},
                )
            else:
                return self.form_invalid(form)
        else:
            return redirect("/")
