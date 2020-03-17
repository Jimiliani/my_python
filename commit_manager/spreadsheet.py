import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


class Spreadsheet:
    def __init__(self, date_from, date_to):
        self.row = 1
        CREDENTIALS_FILE = 'github-commit-monitoring-2fec3435b343.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        self.spreadsheet = self.service.spreadsheets().create(body={
            'properties': {'title': 'Список сделавших коммит с' + date_from + ' по ' + date_to, 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                       'sheetId': 0,
                                       'title': 'Репозитории',
                                       'gridProperties': {'rowCount': 30, 'columnCount': 3}}}]
        }).execute()
        driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)
        shareRes = driveService.permissions().create(
            fileId=self.spreadsheet['spreadsheetId'],
            body={'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
            fields='id'
        ).execute()

    def add_line(self, surname, name, link):
        results = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "Репозитории!" + "A" + str(self.row) + ":C" + str(self.row),
                     "majorDimension": "ROWS",
                     "values": [[surname, name, link]]}]
            }).execute()
        self.row += 1

    def get_link(self):
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet['spreadsheetId']
