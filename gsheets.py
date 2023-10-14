import gspread
import pandas as pd

import config

sa = gspread.oauth(credentials_filename=config.CREDS)
sh = sa.open(config.WKB)

wks = sh.worksheet(title="Allocation")

df = pd.DataFrame(wks.get_all_records())
print(df)
print(df.info())
