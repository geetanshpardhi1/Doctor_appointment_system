from googleapiclient.discovery import build
from datetime import datetime, timedelta,date
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_calendar_event(doctor_email, patient_name, appointment_date, start_time, end_time):
    # Load the credentials file for your Google Cloud project
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
  
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "/home/geetansh/intern_task/task1/credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
   
    start_datetime = f"{appointment_date}T{start_time}"
    end_datetime = f"{appointment_date}T{end_time}"
    
    
    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    
    
    
    event = {
        'summary': f'Appointment with {patient_name}',
        'description': f'Appointment with {patient_name}',
    'start': {
    'dateTime': start_datetime,
    'timeZone': 'UTC',
  },
  'end': {
    'dateTime': end_datetime,
    'timeZone': 'UTC',
  },
  'recurrence': [
  ],
  'attendees': [
    {'email': doctor_email},
    
  ],
  'reminders': {},
}

    event = service.events().insert(calendarId='primary', body=event).execute()
    # print 'Event created: %s' % (event.get('htmlLink'))