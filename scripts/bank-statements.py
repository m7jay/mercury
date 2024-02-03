import tabula
from datetime import datetime, date
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel
from babel.numbers import format_currency, parse_decimal, NumberFormatError


class Transaction(BaseModel):
    txn_date: date
    txn_id: str
    amt_withdrawn: Optional[float]
    amt_deposited: Optional[float]
    balance: float
    others: Optional[str]


tables = tabula.read_pdf(
    "/.../file_path",
    pages="all",
    password="xxx",
    multiple_tables=True,
)


def fmt_data(input: pd.Series) -> pd.Series:
    data = input.copy(deep=True)
    try:
        data.update(
            {
                "txn_date": datetime.strptime(data["txn_date"], "%d-%m-%Y").date(),
                "withdrawls": float(data["withdrawls"]) if data["withdrawls"] else 0.0,
                "deposits": float(data["deposits"]) if data["deposits"] else 0.0,
                "balance": float(data["balance"]) if data["balance"] else 0.0,
            }
        )

    except ValueError:
        pass
    return data


def fmt_amt(amount: float, currency: str, locale: str = "en_IN"):
    return format_currency(amount, currency, locale=locale)


def parse_amt(amount: str, locale: str = "en_IN") -> float:
    if pd.isna(amount):
        return 0.0
    try:
        parsed_amount = parse_decimal(str(amount), locale=locale)
    except NumberFormatError as error:
        parsed_amount = 0.0
    return parsed_amount


def get_merged_tables(tables: List[pd.DataFrame]) -> pd.DataFrame:
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


def get_transactions(tables: List[pd.DataFrame]) -> List[Transaction]:
    transactions_table = get_merged_tables(tables)
    transactions_table.to_excel("txn_table.xlsx", index=False)
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
                Transaction(
                    txn_date=datetime.strptime(txn_date, "%d-%m-%Y").date(),
                    txn_id=txn,
                    amt_withdrawn=parse_amt(withdrawls),
                    amt_deposited=parse_amt(deposits),
                    balance=parse_amt(balance),
                    others=others if not pd.isna(others) else None,
                )
            )
        except ValueError:
            if txn_date == "Txn Date" or txn_date == "Account Statement":
                continue
            raise
    return transactions


txns = get_transactions(tables=tables)

expenses = 0.0
income = 0.0
balance = 371535.33

for txn in txns:
    expenses += round(txn.amt_withdrawn, 2)
    income += round(txn.amt_deposited, 2)
    balance = balance + txn.amt_deposited - txn.amt_withdrawn
    txn.balance = balance

res = pd.DataFrame([txn.model_dump() for txn in txns])
res.to_excel("res2.xlsx", index=False)
