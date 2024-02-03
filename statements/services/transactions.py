from statements.pydantic import TransactionEntity
import tabula
from datetime import datetime
import pandas as pd
from typing import List
from babel.numbers import format_currency, parse_decimal, NumberFormatError
from django.contrib.auth import get_user_model
from statements.models import Statement, Transaction
from typing import Dict, List
import time

User = get_user_model()


def _fmt_amt(amount: float, currency: str, locale: str = "en_IN"):
    return format_currency(amount, currency, locale=locale)


def _parse_amt(amount: str, locale: str = "en_IN") -> float:
    if pd.isna(amount):
        return 0.0
    try:
        parsed_amount = parse_decimal(str(amount), locale=locale)
    except NumberFormatError as error:
        parsed_amount = 0.0
    return parsed_amount


def _get_merged_tables(tables: List[pd.DataFrame]) -> pd.DataFrame:
    table_columns = [
        "txn_date",
        "txn",
        "withdrawls",
        "deposits",
        "balance",
        "others",
    ]
    tables_to_concat = []
    for table in tables[2:-2]:
        table = table.iloc[:, :6]
        if "txn_date" not in table.columns:
            columns = table.columns
            new_row = pd.DataFrame(
                data={
                    "txn_date": [columns[0]],
                    "txn": [columns[1]],
                    "withdrawls": [columns[2]],
                    "deposits": [columns[3]],
                    "balance": [columns[4]],
                    "others": [columns[5]],
                },
                columns=table_columns,
            )
            table.columns = table_columns
            table = pd.concat([new_row, table], ignore_index=True)
        tables_to_concat.append(table)
    return pd.concat(tables_to_concat, ignore_index=True)


def get_transactions(file_path: str, password: str = None) -> List[TransactionEntity]:
    tables = tabula.read_pdf(
        file_path,
        pages="all",
        password=password,
        multiple_tables=True,
    )

    transactions_table = _get_merged_tables(tables)
    transactions = []
    transactions_table.dropna(subset=["txn_date"], inplace=True)
    transactions_table.sort_values(by="txn_date")
    for _, row in transactions_table.iterrows():
        txn_date, txn, withdrawls, deposits, balance, others = (
            row["txn_date"],
            row["txn"],
            row["withdrawls"],
            row["deposits"],
            row["balance"],
            row["others"],
        )
        try:
            transactions.append(
                TransactionEntity(
                    transaction_date=datetime.strptime(txn_date, "%d-%m-%Y").date(),
                    transaction_id=txn,
                    amount_withdrawn=_parse_amt(withdrawls),
                    amount_deposited=_parse_amt(deposits),
                    balance=_parse_amt(balance),
                    others=others if not pd.isna(others) else None,
                )
            )
        except ValueError:
            if txn_date == "Txn Date" or txn_date == "Account Statement":
                continue
            raise
    return transactions


def get_transactions_from_uploaded_file(
    name: str, file_obj: str, password: str = None
) -> List[TransactionEntity]:
    tables = tabula.read_pdf(
        file_obj,
        pages="all",
        password=password,
        multiple_tables=True,
    )

    transactions_table = _get_merged_tables(tables)
    transactions = []
    transactions_table.dropna(subset=["txn_date"], inplace=True)
    transactions_table.sort_values(by="txn_date")
    for _, row in transactions_table.iterrows():
        txn_date, txn, withdrawls, deposits, balance, others = (
            row["txn_date"],
            row["txn"],
            row["withdrawls"],
            row["deposits"],
            row["balance"],
            row["others"],
        )
        try:
            transactions.append(
                TransactionEntity(
                    transaction_date=datetime.strptime(txn_date, "%d-%m-%Y").date(),
                    transaction_id=txn,
                    amount_withdrawn=_parse_amt(withdrawls),
                    amount_deposited=_parse_amt(deposits),
                    balance=_parse_amt(balance),
                    others=others if not pd.isna(others) else None,
                )
            )
        except ValueError:
            if txn_date == "Txn Date" or txn_date == "Account Statement":
                continue
            raise
        time.sleep(1)
    return transactions


def create_or_update_transactions(
    name: str, transactions: List[TransactionEntity], user: User
):
    # create statements
    statements_to_create = dict()
    for transaction in transactions:
        month_str = f"{transaction.transaction_date.year}-{transaction.transaction_date.month}-01"
        if month_str not in statements_to_create:
            statements_to_create[month_str] = list()
        statements_to_create[month_str].append(transaction)

    transactions_to_create = []
    for month_str, monthly_transactions in statements_to_create.items():
        statement, is_created = Statement.objects.update_or_create(
            user=user, month=month_str, defaults={"name": name}
        )
        existing_transactions_ids = []
        if not is_created:
            existing_transactions_ids = list(
                statement.transactions.all().values_list("transaction_id", flat=True)
            )
        for transaction in monthly_transactions:
            if transaction.transaction_id not in existing_transactions_ids:
                transactions_to_create.append(
                    Transaction(
                        transaction_id=transaction.transaction_id,
                        transaction_date=transaction.transaction_date,
                        amount_deposited=transaction.amount_deposited,
                        amount_withdrawn=transaction.amount_withdrawn,
                        balance=transaction.balance,
                        others=transaction.others,
                        statement=statement,
                    )
                )
    # create transactions
    if transactions_to_create:
        Transaction.objects.bulk_create(transactions_to_create)
    return Statement.objects.filter(month__in=statements_to_create, user=user)
