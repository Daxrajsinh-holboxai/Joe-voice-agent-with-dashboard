from datetime import datetime, timedelta
import os.path
from zoneinfo import ZoneInfo
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_busy_times(start_time, end_time):
    creds = get_creds()
    try:
        service = build("calendar", "v3", credentials=creds)
        # Call the Calendar API
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        busy_times = []

        if not events:
            busy_times.append("No upcoming events found for the specified time range.")
            return busy_times
        
        # Extract the busy times (start and end times) from each event
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            
            start_time = datetime.datetime.fromisoformat(start)
            end_time = datetime.datetime.fromisoformat(end)

            start_time_denver = start_time.astimezone(ZoneInfo("America/Denver"))
            end_time_denver = end_time.astimezone(ZoneInfo("America/Denver"))
            # Append the busy time in the format: "from [start_time] to [end_time]"
            busy_times.append(f"from {start_time_denver} to {end_time_denver}")
        
        return busy_times

    except HttpError as error:
        print(f"An error occurred: {error}")
        return ["An error occurred while retrieving events."]


def create_new_booking(patient_name,start_time, email_address):
    creds = get_creds()
    try:
        service = build("calendar", "v3", credentials=creds)
        start_dt = datetime.fromisoformat(start_time)
        end_dt = start_dt + timedelta(hours=1)
        end_time = end_dt.isoformat()
        event = {
            'summary': f'Appointment with {patient_name}',
            'location': '8753 Yates Drive, Suite 110, Westminster, CO',
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Denver',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Denver',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'attendees': [
                {'email': email_address},
                {'email': 'vishnu.nair@holbox.ai'}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s',  event.get('htmlLink'))
        return True
    except Exception as error:
        print("Error Creating New Event: ", error)
        return False


