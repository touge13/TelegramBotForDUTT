import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
import gspread

CREDENTIALS_FILE = 'C://Users/pc1/Desktop/robobot/googlesheets/botdutttelegram-9c0cba3e1c28.json'  # Имя файла с закрытым ключом, вы должны скачать свой такой файл

#создание новой google таблицы
# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'regs', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'regs',
                               'gridProperties': {'columnCount': 11}}}]
}).execute()
spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'duttbottelegram@mail.ru'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()