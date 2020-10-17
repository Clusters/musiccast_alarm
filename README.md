# Musiccast Alarm
Internet radio alarm for Yamahas Musiccast system. Aware of holidays and weekends.
Turns on Yamaha Musiccast loudspeaker and starts the last configured internet radio channel. Starting with a low volume and increments the volume every 10 minutes. After one hour the loudspeaker will be turned off/in standby.

## requirements
- Python 3.7 or later
- The google oAuth libraries. If you use pip perform following command `sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

## config
- you need to set your configuration in example_config.json inside the folder config (details see below).
- you need to create a credentials.json file in the folder googleCalendar. You need to generate one via your Google account (details see below).
- on first login, you will receive a URL which redirects you to Googles oauth service. Login with your account and call the URL you become redirected to, in a browser or wget on the machine where you actually run Musiccast Alarm on.

### config.json file
- "ip_address": 

   The IP address of the Musiccast loudspeaker

- "yamaha_system_volume_factor":

   Every Yamaha loudspeaker has other volume characteristics. So a volume set for a WX-030-1 can be too loud or too silent on other Musiccast loudspeakers. To compensate this you can modify the volume by changing this factor. A higher value will increase the total volume, while a lower value will decrease the volume. A value of 1 is good for a WX-030-1 loudspeaker for instance.

   ATTENTION! Some Musiccast devices might not have a percentage based volume indication (which was tested by myself). For instance audio receivers like the R-N803D might have a dB based volume indication. This would mean that there are signed (negative and positive) numbers possible. If so, even a very small value like 0.0001 would basically blow your roof off, if you have decent loudspeakers connected to it. Using such Musiccast devices is at your own risk (like everything else, as I cannot test everything with my zero-budget). You have been warned.

   If you have a receiver and unsure if it will work, I would recommend to disconnect the speakers, make a test and read the volume set by the Alarm.

- "routine_start_hour":

   At which hour of the day the alarm should go off? (24h format)

- "routine_start_minute":

   At which minute of the day the alarm should go off? Because some Musiccast loudspeakers have a delay, the acutal music starts some seconds after this time was reached.

- "vacation_calendar_id":

   The calendar ID of the calender were you enter your personal holidays (vacation days). You can find the ID on Google in your calendar settings (look under integrate calendar). This can also be an email address. It depends on how you created the calendar.

- "vacation_keyword": 

   If your calendar not only contains vacation days, define here which keyword the relevant items have. Set it to null without "" if your calendar only contains relevant entries.

- "holiday_calender_id":

   Same as holiday_calender_id, just for your federal and religious holidays. If you use only one calender which exclusevily contains all relevant holidays you can also set this to null.

- "holiday_keyword":

   Same as vacation_keyword.

### credentials.json file
You can find the Google page here [https://console.developers.google.com/apis/credentials]

Create and download an OAuth 2.0-Client-ID, rename the file to credentials.json and move it to the Apps googleCalendar folder.