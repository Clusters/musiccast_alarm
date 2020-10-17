import datetime
import pickle
import os.path
from googleapiclient.discovery import build # sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from libs.helpers import get_config

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class GoogleCalendar:
    config = get_config()

    """Implements the GoogleCalendar API and authenticates with my personal Google Calendar"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(path + '/token.pickle'):
        with open(path + '/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(path + '/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path + '/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    midnight = \
        datetime.datetime.replace(
            datetime.datetime.now(), hour=23, minute=59, second=59
        ).astimezone().isoformat()

    def is_holiday_today(self) -> bool:
        """Requests from my Google Calendars if today is a personal or public holiday

        :return: True if today is a holiday, otherwise false
        """
        return self._is_personal_holiday_today or self._is_public_holiday_today()

    @property
    def _is_personal_holiday_today(self) -> bool:
        """Requests from the Google Calendar "Arbeit Arbeit" if today is a personal holiday

        :return: True if today is a holiday, otherwise false
        """
        if self.config["vacation_keyword"] is not None:
            events_result = self.service.events().list(
                calendarId=self.config["vacation_calendar_id"],  # calendar "Arbeit Arbeit"
                timeMin=self.now,
                timeMax=self.midnight,
                q=self.config["vacation_keyword"],
                maxResults=10
            ).execute()
        else:
            events_result = self.service.events().list(
                calendarId=self.config["vacation_calendar_id"],  # calendar "Arbeit Arbeit"
                timeMin=self.now,
                timeMax=self.midnight,
                maxResults=10
            ).execute()

        today_is_holiday = events_result.get('items', []).__len__() > 0

        if today_is_holiday:
            print("Today is a private holiday")
        else:
            print("Today is not a private holiday")

        return today_is_holiday

    def _is_public_holiday_today(self) -> bool:
        """Requests from the Google Calendar "Gesetzliche Feiertage" if today is a public holiday (for my business)

        :return: True if today is a holiday, otherwise false
        """
        if self.config["holiday_calender_id"] is None:
            return False
        
        if self.config["holiday_keyword"] is not None:
            events_result = self.service.events().list(
                calendarId=self.config["holiday_calender_id"],  # calendar "Gesetzliche Feiertage"
                timeMin=self.now,
                timeMax=self.midnight,
                q=self.config["holiday_keyword"],
                maxResults=10
            ).execute()
        else:
            events_result = self.service.events().list(
                calendarId=self.config["holiday_calender_id"],  # calendar "Gesetzliche Feiertage"
                timeMin=self.now,
                timeMax=self.midnight,
                maxResults=10
            ).execute()

        today_is_holiday = events_result.get('items', []).__len__() > 0

        if today_is_holiday:
            print("Today's public holiday is %s" % events_result.get('items', [])[0]['summary'])
        else:
            print("Today is not a public holiday")

        return today_is_holiday
