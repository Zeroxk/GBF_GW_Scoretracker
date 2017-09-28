from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery,errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from time import sleep

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GW matchscore tracker'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gw.matchscore.tracker.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def write_to_sheet(myScore, oppScore, current_time, usOnline, oppOnline):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1N8KaYe7a3VLcbPz3VLwdMeUXcq5GR3fLlqPGj4NbMoE'
    range_name = 'Day5!A:C'

    values = [
        [
            current_time, myScore, oppScore
        ]
    ]
    
    body = {
        'values': values
    }

    try:
        result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()
    except errors.HttpError as err:
        print("Error when writing to sheet {}, retrying after 30s".format(err.))
        sleep(30)
        write_to_sheet(myScore,oppScore,current_time,usOnline,oppOnline)
        

    

def main():
    write_to_sheet(100, 99, '01:02:03', 3, 4)

if __name__ == '__main__':
    main()