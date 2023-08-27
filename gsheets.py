import gspread

import config

sa = gspread.oauth(credentials_filename=config.CREDS)
sh = sa.open(config.WKB)

wks = sh.worksheet()
