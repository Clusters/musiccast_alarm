import datetime
import os
import time

import requests

from googleCalendar.GoogleCalendar import GoogleCalendar
from libs.helpers import get_config


class Alarm:
    "Alarm main class"
    config = get_config()

    def wait_till_next_day(self) -> None:
        """Wait till tomorrow"""
        print(
            "%s -> wait till next day %s:%s o'clock" % (
                datetime.datetime.now().astimezone().isoformat(),
                self.config["routine_start_hour"],
                self.config["routine_start_minute"]
                )
            )
        tomorrow = datetime.datetime.replace(
            datetime.datetime.now().astimezone() + datetime.timedelta(days=1),
            hour=self.config["routine_start_hour"], 
            minute=self.config["routine_start_minute"], 
            second=0
        )
        delta = tomorrow - datetime.datetime.now().astimezone()
        time.sleep(delta.seconds)
        print("Wait completed. It is now " + datetime.datetime.now().astimezone().isoformat())

    def wait_till_given_time(self, hour: int, minute: int) -> None:
        """DEBUG function: Wait until given time"""
        print("%s -> wait till today %s:%s" % (datetime.datetime.now().astimezone().isoformat(), hour, minute))
        today_given_time = datetime.datetime.replace(datetime.datetime.now().astimezone(),
                                                    hour=hour, minute=minute, second=0)
        delta = today_given_time - datetime.datetime.now().astimezone()
        time.sleep(delta.seconds)
        print("Wait completed. It is now " + datetime.datetime.now().astimezone().isoformat())

    def is_workday(self) -> bool:
        """Check if weekend, holiday or vacation does not apply

        :return: True if today is a working day, otherwise False
        """
        is_weekday = datetime.datetime.now().isoweekday() < 6

        if not is_weekday:
            print("Today is no weekday.")
            return False

        if GoogleCalendar().is_holiday_today():
            return False

        print("Today is a workday.")
        return True

    def play_radio(self) -> None:
        """Launches and plays the Internet Radio on a Yamaha loudspeaker. Starts with low volume and increases it.
        Turns off the loudspeakers an hour after this method was called.

        :return: None
        """
        ip_address = self.config["ip_address"]  # YAMAHA audio device
        api_base_url = 'http://%s/YamahaExtendedControl/v1/' % ip_address
        yamaha_system_volume_factor = self.config["yamaha_system_volume_factor"] # e.g. 1 for WX-030-1

        # power on device
        print("power on device")
        requests.get(api_base_url + 'main/setPower?power=on')

        time.sleep(2)

        # set volume to quiet
        print("set volume to quiet")
        requests.get(api_base_url + 'main/setVolume?volume=%s' % round(5 * yamaha_system_volume_factor))

        time.sleep(2)

        # start internet radio
        print("start internet radio")
        requests.get(api_base_url + 'main/setInput?input=net_radio')
        time.sleep(2)
        requests.get(api_base_url + 'netusb/setPlayback?playback=play')

        # wait for 10 minutes and increase volume
        print("wait for 10 minutes and increase volume to %s" % round(7 * yamaha_system_volume_factor))
        time.sleep((60 * 10 - 6))
        requests.get(api_base_url + 'main/setVolume?volume=%s' % round(7 * yamaha_system_volume_factor))
        print("volume increased to %s" % round(7 * yamaha_system_volume_factor))

        # wait for 10 minutes and increase volume
        print("wait for 10 minutes and increase volume to %s" % round(10 * yamaha_system_volume_factor))
        time.sleep((60 * 10))
        requests.get(api_base_url + 'main/setVolume?volume=%s' % round(10 * yamaha_system_volume_factor))
        print("volume increased to %s" % round(10 * yamaha_system_volume_factor))

        # wait for 10 minutes and increase volume
        print("wait for 10 minutes and increase volume to %s" % round(14 * yamaha_system_volume_factor))
        time.sleep((60 * 10))
        requests.get(api_base_url + 'main/setVolume?volume=%s' % round(14 * yamaha_system_volume_factor))
        print("volume increased to %s" % round(14 * yamaha_system_volume_factor))

        # wait for 10 minutes and increase volume
        print("wait for 10 minutes and increase volume to %s" % round(17 * yamaha_system_volume_factor))
        time.sleep((60 * 10))
        requests.get(api_base_url + 'main/setVolume?volume=%s' % round(17 * yamaha_system_volume_factor))
        print("volume increased to %s" % round(17 * yamaha_system_volume_factor))

        # wait for 10 minutes and increase volume
        print("wait for 10 minutes and increase volume to %s" % round(20 * yamaha_system_volume_factor))
        time.sleep((60 * 10))
        requests.get(api_base_url + 'main/setVolume?volume=%s' % round(20 * yamaha_system_volume_factor))
        print("volume increased to %s" % round(20 * yamaha_system_volume_factor))

        # wait for 10 minutes and stop radio
        print("wait for 10 minutes and stop radio")
        time.sleep((60 * 10))
        print("Lower volume to %s and set loudspeaker to standby" % round(5 * yamaha_system_volume_factor))
        requests.get(api_base_url + 'main/setVolume?volume=%s' % round(5 * yamaha_system_volume_factor))
        time.sleep(1)
        requests.get(api_base_url + 'main/setPower?power=standby')


alarm = Alarm()

while True:
    alarm.wait_till_next_day()
    #alarm.wait_till_given_time(22, 18)

    print("### Ping check to target oauth2.googleapis.com ###")
    # necessary for embedded devices like the Raspberry Pi Zero W
    os.system("ping -c 1 oauth2.googleapis.com")

    if alarm.is_workday():
        alarm.play_radio()
    else:
        time.sleep(1) # to avoid spamming workday checks against googles API
