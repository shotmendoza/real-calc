from abc import abstractmethod, ABC
from pathlib import Path
from typing import Optional

import pandas as pd

import config


class Bank(ABC):
    _root_folder = config.REPORTS_FOLDER_FROM_ROOT

    @abstractmethod
    def open_statement(self, statement_path: Path, *args, **kwargs) -> pd.DataFrame:
        """Should open the bank statement for the given bank

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
