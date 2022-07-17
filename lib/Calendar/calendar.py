from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_events( creds, timeRange ):
    # The file token.json stores the user's access and refresh tokens
    try:
        service = build('calendar', 'v3', credentials=creds)
        # Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Select the range you want to see')
        # range = input();
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=timeRange, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            # print('No upcoming events found.')
            return None, "No upcoming events found." 

        # Prints the start and name of the events
        # for event in events:
        #     start = event['start'].get('dateTime', event['start'].get('date'))
        #     print(start, event['summary'])
        return events, None

    except HttpError as error:
        # print('An error occurred: %s' % error)
        return None, sprint('An error occurred: %s' % error)

if __name__ == '__main__':
    get_events()
