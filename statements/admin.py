from django.contrib import admin

from .models import Transaction, Statement

admin.register(Transaction)
admin.register(Statement)
