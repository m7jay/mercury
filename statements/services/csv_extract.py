import csv
from io import StringIO
from typing import List
from datetime import datetime
from statements.pydantic import TransactionEntity
from main.utils.amount import parse_amount


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
                    amount_deposited=parse_amount(row[4]),
                    amount_withdrawn=parse_amount(row[3]),
                    balance=parse_amount(row[5]),
                    others=None,
                )
            )
    return transactions
