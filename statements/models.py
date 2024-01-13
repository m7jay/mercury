from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Statement(models.Model):
    month = models.DateField(blank=False, null=False)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)


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
    others = models.TextField(null=True)

    statement = models.ForeignKey(to=Statement, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["statement_id", "transaction_id"],
                name="unique-transaction-for-statement",
            )
        ]
