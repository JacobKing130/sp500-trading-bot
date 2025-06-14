import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Path to your Google API credentials JSON
CREDENTIALS_PATH = 'credentials.json'  # You need to download this from Google Cloud Console

# Google Sheets info (update with your sheet name and worksheet)
SPREADSHEET_NAME = 'TradingJournal'
WORKSHEET_NAME = 'Trades'

def log_to_google_sheets(trades_df: pd.DataFrame, summary: dict, asset: str):
    # Authenticate with Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet and worksheet
    sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

    # Prepare data to append: convert dataframe to list of lists
    # Add asset info as a new column before exporting
    trades_df['Asset'] = asset
    trades_data = trades_df.fillna('').values.tolist()

    # Append rows to sheet
    for row in trades_data:
        sheet.append_row(row)

    # Optionally, you can update a summary worksheet or cells with summary info here

