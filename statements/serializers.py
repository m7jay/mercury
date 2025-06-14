from rest_framework import serializers
from statements.models import Statement, Transaction
from main.utils.amount import format_amount


class StatementSerializer(serializers.ModelSerializer):
    transactions_count = serializers.SerializerMethodField()
    opening_balance = serializers.SerializerMethodField()
    closing_balance = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    id = serializers.UUIDField(source="unique_id")
    total_expenses = serializers.SerializerMethodField()

    def get_month(self, statement):
        return statement.month.strftime("%b - %Y")

    def get_transactions_count(self, statement):
        return statement.transactions.count()

    def get_opening_balance(self, statement):
        first_transaction: Transaction = (
            statement.transactions.all().order_by("transaction_date").first()
        )
        # revert the first transaction to get the opening balance
        return (
            (
                first_transaction.balance
                - first_transaction.amount_deposited
                + first_transaction.amount_withdrawn
            )
            if first_transaction
            else 0
        )

    def get_closing_balance(self, statement):
        transaction: Transaction = (
            statement.transactions.all().order_by("-transaction_date").first()
        )
        return transaction.balance if transaction else 0

    def get_total_expenses(self, statement):
        total_expenses = 0
        for transaction in statement.transactions.all():
            total_expenses += transaction.amount_withdrawn
        return round(total_expenses, 2)

    class Meta:
        model = Statement
        fields = [
            "id",
            "month",
            "user_id",
            "transactions_count",
            "opening_balance",
            "closing_balance",
            "total_expenses",
        ]


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "transaction_date",
            "amount_deposited",
            "amount_withdrawn",
            "balance",
            "others",
        ]
