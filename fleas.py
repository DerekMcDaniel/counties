from googleplaces import GooglePlaces, types, lang
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

creds = r"C:\Users\Derek\PycharmProjects\creds.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)

gc = gspread.authorize(credentials)

# try:
#     sh = gc.create('GA Rehab')
#     sh.share('zzz@gmail.com', perm_type='user', role='writer')
# except:
#     sh = gc.open('GA Rehab')

sh = gc.open('GA Rehab')

worksheet = sh.sheet1

YOUR_API_KEY = ''

google_places = GooglePlaces(YOUR_API_KEY)

value_list = []

search_term = "health+and+rehabilitation+"

with open('+GA', 'r') as infile:
    for value in infile.readlines():
        value_list.append(value)

value_list = [search_term + x.strip('\n') for x in value_list]
# value_list = value_list[0:10]

class Finder:
    row = 2
    count = 0

    def check_next(self, next_page):
            for place in next_page.places:
                place.get_details()
                self.count += 1
                print(self.count, 'NEXT PAGE')
                range_build = 'A' + str(self.row) + ':G' + str(self.row)
                cell_list = worksheet.range(range_build)
                cell_list[0].value = place.name
                cell_list[1].value = place.formatted_address
                cell_list[2].value = place.local_phone_number
                cell_list[3].value = place.website
                cell_list[4].value = place.geo_location
                cell_list[5].value = place.url
                cell_list[6].value = place.rating
                worksheet.update_cells(cell_list)
                self.row += 1
                if next_page.has_next_page_token:
                    sleep(2)
                    next_page = google_places.text_search(
                        pagetoken=next_page.next_page_token)
                    self.check_next(next_page)

    def get_places(self):
        for value in value_list:
            query_result = google_places.text_search(query=value)
            for place in query_result.places:
                place.get_details()
                self.count += 1
                print(self.count)
                gc.login()
                range_build = 'A' + str(self.row) + ':G' + str(self.row)
                cell_list = worksheet.range(range_build)
                cell_list[0].value = place.name
                cell_list[1].value = place.formatted_address
                cell_list[2].value = place.local_phone_number
                cell_list[3].value = place.website
                cell_list[4].value = place.geo_location
                cell_list[5].value = place.url
                cell_list[6].value = place.rating
                worksheet.update_cells(cell_list)
                self.row += 1
                if query_result.has_next_page_token:
                    sleep(2)
                    next_page = google_places.text_search(
                        pagetoken=query_result.next_page_token)



get_place = Finder()
get_place.get_places()
