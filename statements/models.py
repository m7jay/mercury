from django.db.models import Model, CharField, DateField, DecimalField, TextField

class Transaction(Model):
    transaction_id = CharField(max_length=1024, null=False, blank=False, db_index=True)
    transaction_date = DateField(blank=False, null=False)
    amount_deposited = DecimalField(max_digits=12, decimal_places=2, null=True, blank=False)
    amount_withdrawn = DecimalField(max_digits=12, decimal_places=2, null=True, blank=False)
    balance = DecimalField(max_digits=12, decimal_places=2, null=True, blank=False)
    others = TextField(null=True)
