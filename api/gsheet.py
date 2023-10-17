import gspread
import pandas as pd


class GSpreadWrapper:
    def __init__(self, credential_path: str, workbook_name: str, sheet_name: str):
        """Wrapper to get data from a google sheet

        :param credential_path: the path to the credentials.json file that was created when setting up the API
        """
        self._oath_credentials = credential_path
        self.workbook = workbook_name
        self.sheet_name = sheet_name

    def read(self) -> pd.DataFrame:
        with gspread.oauth(credentials_filename=self._oath_credentials).open(self.workbook) as wkb:
            wks = wkb.worksheet(title=self.sheet_name)
            df = pd.DataFrame(wks.get_all_records())
        return df

    def update(self, df: pd.DataFrame) -> None:
        with gspread.oauth(credentials_filename=self._oath_credentials).open(self.workbook) as wkb:
            wks = wkb.worksheet(title=self.sheet_name)
            wks.update([df.columns.values.tolist()] + df.values.tolist())
        return None
