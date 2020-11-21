from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery,errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from time import sleep

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gbf-gw-scoretracker'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    try:
        import argparse
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags, extras = parser.parse_known_args()
    except ImportError:
        flags = None

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gw.scoretracker.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def setup(spreadsheetId):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    global service
    service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)
    global SPREADSHEET_ID
    SPREADSHEET_ID = spreadsheetId

def write_to_sheet(values, ranges):
    
    range_name = ranges
    
    body = {
        'values': values
    }

    try:
        result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()
    except errors.HttpError as err:
        print("Error when writing to sheet {}, retrying after 30s".format(err))
        sleep(30)
        write_to_sheet(values, ranges)

def get_spreadSheets():
    return service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, ranges=None, includeGridData=None).execute()

def get_worksheets():
    spreadSheet = get_spreadSheets()
    return spreadSheet["sheets"]

def worksheet_exists(worksheetName):
    worksheets = get_worksheets()

    for worksheet in worksheets:
        if worksheet["properties"]["title"] == worksheetName:
            return True

    return False

def create_new_worksheet(worksheetName):
    body = {
        ""
    }
    service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
    return None

        
def main():

    setup('1ZFcc8xSPOuM2epcevbfAMSVWQb3CFIGNpxHhH4v5jjc')

    values = [
        [
            100, 99, '01:02:03'
        ]
    ]
    worksheet_exists("Day1")
    write_to_sheet(values, 'Day1!A:C')

if __name__ == '__main__':
    main()