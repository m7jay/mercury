from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Statement(models.Model):
    name = models.CharField(max_length=128, null=True)
    month = models.DateField(blank=False, null=False)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["month", "user_id"],
                name="unique-statement-for-user",
            )
        ]


class Transaction(models.Model):
    transaction_id = models.CharField(
        max_length=1024, null=False, blank=False, db_index=True
    )
    transaction_date = models.DateField(blank=False, null=False)
    amount_deposited = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=False
    )
    amount_withdrawn = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=False
    )
    balance = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=False
    )
    others = models.TextField(null=True, max_length=2048)

    statement = models.ForeignKey(
        to=Statement, related_name="transactions", on_delete=models.PROTECT
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["statement_id", "transaction_id"],
                name="unique-transaction-for-statement",
            )
        ]
