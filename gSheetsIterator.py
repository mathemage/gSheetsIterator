# based on quickstart.py at https://developers.google.com/sheets/api/quickstart/python
from __future__ import print_function

import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API'


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
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def connect():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service


def get_sheet_content(service, spreadsheet_id='1QIltp_iIDwlI5dVQUovocmB89nglJTVBJjEFac46APU'):
    '''
    :return: return list of rows, where each row is again list of cell values
    '''
    range_name = 'Sheet1!A:C'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    content = result.get('values', [])
    return content


def display_content(content):
    if not content:
        print('No data found.')
    else:
        heading = content[0]
        entries = content[1:]
        print('%s, %s, %s: ' % (heading[0], heading[1], heading[2]))
        for row in entries:
            print('%s, %s, %s' % (row[0], row[1], row[2]))


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1QIltp_iIDwlI5dVQUovocmB89nglJTVBJjEFac46APU/
    """
    service = connect()

    content = get_sheet_content(service)
    print('Sheet ID: 1QIltp_iIDwlI5dVQUovocmB89nglJTVBJjEFac46APU')
    display_content(content)

    print()

    print('Sheet ID: 1MFIzsbXBjiELmyLrEDRfxXjmSKkVY-qs_MfED0vWP_I')
    content = get_sheet_content(service, spreadsheet_id='1MFIzsbXBjiELmyLrEDRfxXjmSKkVY-qs_MfED0vWP_I')
    display_content(content)


if __name__ == '__main__':
    main()
