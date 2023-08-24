import pandas as pd

import config
from api.banks import BestBuy, WellsFargo, AmericanExpress


def test_amex():
    path = config.REPORTS_FOLDER_FROM_ROOT / "activity.csv"
    amex = AmericanExpress()
    df = amex.open_statement(path)
    print(df)
    print(df.info())
    print(df["Amount"].sum())


def test_best_buy():
    path = config.REPORTS_FOLDER_FROM_ROOT / "06-02-2023 BB.csv"
    print(path.exists())
    bb = BestBuy()
    df = bb.open_statement(path)
    print(df)
    print(df["amount"].sum())


def test_wells_fargo_cc():
    path = config.REPORTS_FOLDER_FROM_ROOT / "CreditCard3 - 03.29.2023 - 06.27.2023.csv"
    wf = WellsFargo()
    df = wf.open_statement(path, tags="credit card")
    print(df)
    print(df.info())
    print(df["amount"].sum())


def test_wells_fargo_d():
    path = config.REPORTS_FOLDER_FROM_ROOT / "Checking1 - 03.2023 - 06.27.2023.csv"
    wf = WellsFargo()
    df = wf.open_statement(path, tags="debit card")
    print(df)
    print(df.info())
    print(df["amount"].sum())
