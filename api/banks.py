from abc import abstractmethod, ABC
from pathlib import Path

import pandas as pd

import config


class Bank(ABC):
    _root_folder = config.REPORTS_FOLDER_FROM_ROOT

    @abstractmethod
    def open_statement(self, statement_path: Path) -> pd.DataFrame:
        """Should open the bank statement for the given bank

        :param statement_path: file path to the bank statement
        :return: the dataframe of the bank statement
        """


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
