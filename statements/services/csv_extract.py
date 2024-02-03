import csv
from io import StringIO
from typing import List
from datetime import datetime
from statements.pydantic import TransactionEntity
from babel.numbers import parse_decimal, NumberFormatError


def _parse_amt(amount: str, locale: str = "en_IN") -> float:
    if not amount:
        return 0.0
    try:
        parsed_amount = parse_decimal(str(amount), locale=locale)
    except NumberFormatError as error:
        parsed_amount = 0.0
    return parsed_amount


def get_transactions_from_csv(file_contents: StringIO) -> List[TransactionEntity]:
    transactions = []
    csv_reader = csv.reader(file_contents)
    transaction_block = False
    for row in csv_reader:
        if "Tran Date" in row:
            transaction_block = True
            continue
        if transaction_block and (not row or len(row) == 0):
            transaction_block = False
        if transaction_block:
            transactions.append(
                TransactionEntity(
                    transaction_id=row[2],
                    transaction_date=datetime.strptime(row[0], "%d-%m-%Y").date(),
                    amount_deposited=_parse_amt(row[4]),
                    amount_withdrawn=_parse_amt(row[3]),
                    balance=_parse_amt(row[5]),
                    others=None,
                )
            )
    return transactions
