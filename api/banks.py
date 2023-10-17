from abc import abstractmethod, ABC
from pathlib import Path
from typing import Optional

import pandas as pd

import config


class Bank(ABC):
    _root_folder = config.REPORTS_FOLDER_FROM_ROOT

    @abstractmethod
    def open_statement(self, statement_path: Path, *args, **kwargs) -> pd.DataFrame:
        """Should open the bank statement for the given bank. Should run a check
        to ensure that the correct bank report is being read.

        *args and  **kwargs based on pandas.read_csv() function

        :param statement_path: file path to the bank statement
        :return: the dataframe of the bank statement
        """


class AmericanExpress(Bank):
    def open_statement(self, statement_path: Path, *args, **kwargs) -> pd.DataFrame:
        df = pd.read_csv(
            statement_path,
            *args,
            **kwargs
        )
        return df


class BestBuy(Bank):
    def open_statement(self, statement_path: Path, *args, **kwargs) -> pd.DataFrame:
        df = pd.read_csv(
            statement_path,
            sep=r"\t",
            header=None,
            names=["transaction_date", "amount", "transaction_name", "transaction_type"],
            *args, **kwargs
        )
        df["amount"] = df["amount"].str.replace("$", "").astype(float).round(5)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.date
        return df


class WellsFargo(Bank):
    def open_statement(self, statement_path: Path, tags: Optional[str] = None, *args, **kwargs) -> pd.DataFrame:
        df = pd.read_csv(
            statement_path,
            header=None,
            names=["transaction_date", "amount", "spacer", "spacer2", "transaction_name"],
            *args, **kwargs
        )
        df["amount"] = df["amount"].astype(float).round(5)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.date
        df["transaction_type"] = [tags for _ in df["transaction_date"]]
        df = df.drop(labels=["spacer", "spacer2"], axis="columns")
        return df


class Chase(Bank):
    @classmethod
    def _confirm_chase_headers(cls, columns: list[str]) -> bool:
        check_for_debit_columns = (
            "Details", "Posting Date",
            "Description", "Amount",
            "Type", "Balance",
            "Check or Slip #"
        )

        check_for_credit_columns = (
            "Card", "Transaction Date",
            "Post Date", "Description",
            "Category", "Type", "Amount",
            "Memo"
        )

        debit_column_flag = False
        credit_column_flag = False
        for required_column in check_for_debit_columns:
            if required_column not in columns:
                break
        for required_column in check_for_credit_columns:
            if required_column not in columns:
                break

        if all((debit_column_flag, credit_column_flag)):
            return False
        return True

    def open_statement(self, statement_path: Path, *args, **kwargs) -> pd.DataFrame:
        df = pd.read_csv(
            statement_path,
            *args,
            **kwargs
        )
        column_set_check = self._confirm_chase_headers(df.columns)
        if column_set_check is False:
            raise KeyError(f"Missing expected Chase csv headers. Please refer to doc for list of expected.")
        return df


class BankOfAmerica(Bank):
    @classmethod
    def _confirm_headers(cls, column: list[str]) -> bool:
        expected_headers = (
            "Posted Date", "Reference Number",
            "Payee", "Address", "Amount"
        )

        for expected in expected_headers:
            if expected not in column:
                raise KeyError(f"Expected {expected}, missing from given path.")
        return True

    def open_statement(self, statement_path: Path, *args, **kwargs) -> pd.DataFrame:
        df = pd.read_csv(
            statement_path,
            *args,
            **kwargs
        )
        column_set_check = self._confirm_headers(df.columns)
        return df
