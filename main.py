from __future__ import print_function
from datetime import datetime
import iso8601, sys, getopt, json, os.path, csv, re, os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from lib.Calendar.calendar import get_events
from lib.Keep.keep import Keep
from dotenv import dotenv_values

SCOPES_CALENDAR = ['https://www.googleapis.com/auth/calendar.readonly']
SCOPES_KEEP = ['https://www.googleapis.com/auth/keep']

def getCredentials(scope):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scope)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

helpString = 'argument needed:\n -t --time-range how many days to look ahead'

def main():

    envar = dotenv_values(".env")

    if not bool(envar):
        with open(".env", "w") as f:
            f.write("KEEPACCOUNT=\nKEEPPASSWORD=")
        print("ERROR: please fill out the .env file with user mail and application password")
        sys.exit(2)

    # getting arguments
    timeRange = -1

    # check for correct amount of arguments
    if len( sys.argv ) != 2:
        print (helpString)
        return

    # get argument, otherwise return error
    try:
        opts, args = getopt.getopt(sys.argv,"ht:",["logout", "time-range="])
    except getopt.GetoptError:
        print (helpString)
        sys.exit(2)

    # loop through arguments
    for opt, arg in opts:
        if opt == '-h':
            print (helpString)
            sys.exit()
        elif opt == "-l":
            os.remove(".env")
            os.remove("token.json")
            print("Logout successfull")
            return
        elif opt in ("-t", "--time-range"):
            timeRange = arg

    # get events
    events, err = get_events(getCredentials(SCOPES_CALENDAR), 7)
    if err != None:
        print(err)
        return

    # get loaded events id
    loadedEvents = {}

    # login in keep
    keepIf = Keep(envar["KEEPACCOUNT"],envar["KEEPPASSWORD"])

    existingNotes = keepIf.getAllNotes()

    for note in existingNotes:
        result = re.search(r"#pya\[(\w+)\]$", note.text)
        if result != None:
        # Extract matching values of all groups
            loadedEvents.update({result.group(1):True})

    # print(loadedEvents)
    # get events to add, exluding those we already added
    eventsToAdd = []

    for ev in events:
        if ev['id'] not in loadedEvents:
            endTime = iso8601.parse_date(ev['end']['dateTime'])
            eventsToAdd.append([ev['id'], endTime.strftime("%Y-%m-%d %H:%M:%S"), ev['summary'], ev['description']])

    print("Loading: "+str(eventsToAdd))

    for event in eventsToAdd:
        keepIf.pushToKeep({ "Title": event[2],"Text": event[3]+"\n#pya["+event[0]+"]"})

if __name__ == "__main__":
    main()
