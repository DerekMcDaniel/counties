import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

creds = r"C:\Users\Derek\PycharmProjects\creds.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)

gc = gspread.authorize(credentials)

sh = gc.open('US Counties')

worksheet = sh.sheet1

values_list = worksheet.col_values(1)

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
STATES = ["+" + x for x in STATES]

for value in values_list:
    for state in STATES:
        if state in value:
            with open(state, 'a', encoding='utf-8') as outfile:
                outfile.write(value + '\n')

