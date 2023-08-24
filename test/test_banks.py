import pandas as pd

import config
from api.banks import BestBuy


def test_best_buy():
    path = config.REPORTS_FOLDER_FROM_ROOT / "06-02-2023 BB.csv"
    print(path.exists())
    bb = BestBuy()
    df = bb.open_statement(path)
    print(df)
    print(df["amount"].sum())
