from rest_framework import serializers
from statements.models import Statement, Transaction


class StatementsSerializer(serializers.ModelSerializer):
    transactions_count = serializers.SerializerMethodField()
    opening_balance = serializers.SerializerMethodField()
    closing_balance = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()

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
            first_transaction.balance
            - first_transaction.amount_deposited
            + first_transaction.amount_withdrawn
        )

    def get_closing_balance(self, statement):
        transaction: Transaction = (
            statement.transactions.all().order_by("-transaction_date").first()
        )
        return transaction.balance

    class Meta:
        model = Statement
        fields = [
            "month",
            "user_id",
            "transactions_count",
            "opening_balance",
            "closing_balance",
        ]
