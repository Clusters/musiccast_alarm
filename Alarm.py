import datetime
import os
import time

import requests

from googleCalendar.GoogleCalendar import GoogleCalendar


def wait_till_next_morning():
    """Wait to tomorrow 06:00"""
    print("wait till next morning 6 o'clock")
    tomorrow_morning = datetime.datetime.replace(datetime.datetime.now().astimezone() + datetime.timedelta(days=1),
                                                 hour=6, minute=0, second=0)
    delta = tomorrow_morning - datetime.datetime.now().astimezone()
    time.sleep(delta.seconds)
    print("Wait completed. It is now " + datetime.datetime.now().astimezone().isoformat())


def wait_till_given_time(hour: int):
    """DEBUG function: Wait until given time"""
    print("wait till today point %s" % hour)
    today_given_time = datetime.datetime.replace(datetime.datetime.now().astimezone(),
                                                 hour=hour, minute=0, second=0)
    delta = today_given_time - datetime.datetime.now().astimezone()
    time.sleep(delta.seconds)
    print("Wait completed. It is now " + datetime.datetime.now().astimezone().isoformat())


def is_workday() -> bool:
    """Check if weekend, holiday or vacation does not apply

    :return: True if today is a working day, otherwise False
    """
    is_weekday = datetime.datetime.now().isoweekday() < 6

    if not is_weekday:
        return False

    if GoogleCalendar().is_holiday_today():
        return False

    return True


def play_radio() -> None:
    """Launches and plays the Internet Radio on my bedroom loudspeakers. Starts with low volume and increases it.
    Turns off the loudspeakers an hour after this method was called.

    :return: None
    """
    ip_address = '192.168.1.58'  # WX-030-1
    api_base_url = 'http://%s/YamahaExtendedControl/v1/' % ip_address
    yamaha_system_volume_factor = 1

    # power on device
    print("power on device")
    requests.get(api_base_url + 'main/setPower?power=on')

    time.sleep(2)

    # set volume to quiet
    print("set volume to quiet")
    requests.get(api_base_url + 'main/setVolume?volume=%s' % (5 * yamaha_system_volume_factor))

    time.sleep(2)

    # start internet radio
    print("start internet radio")
    requests.get(api_base_url + 'main/setInput?input=net_radio')
    time.sleep(2)
    requests.get(api_base_url + 'netusb/setPlayback?playback=play')

    # wait for 10 minutes and increase volume
    print("wait for 10 minutes and increase volume to %s" % (7 * yamaha_system_volume_factor))
    time.sleep((60 * 10 - 6))
    requests.get(api_base_url + 'main/setVolume?volume=%s' % (7 * yamaha_system_volume_factor))
    print("volume increased to %s" % (7 * yamaha_system_volume_factor))

    # wait for 10 minutes and increase volume
    print("wait for 10 minutes and increase volume to %s" % (10 * yamaha_system_volume_factor))
    time.sleep((60 * 10))
    requests.get(api_base_url + 'main/setVolume?volume=%s' % (10 * yamaha_system_volume_factor))
    print("volume increased to %s" % (10 * yamaha_system_volume_factor))

    # wait for 10 minutes and increase volume
    print("wait for 10 minutes and increase volume to %s" % (14 * yamaha_system_volume_factor))
    time.sleep((60 * 10))
    requests.get(api_base_url + 'main/setVolume?volume=%s' % (14 * yamaha_system_volume_factor))
    print("volume increased to %s" % (14 * yamaha_system_volume_factor))

    # wait for 10 minutes and increase volume
    print("wait for 10 minutes and increase volume to %s" % (17 * yamaha_system_volume_factor))
    time.sleep((60 * 10))
    requests.get(api_base_url + 'main/setVolume?volume=%s' % (17 * yamaha_system_volume_factor))
    print("volume increased to %s" % (17 * yamaha_system_volume_factor))

    # wait for 10 minutes and increase volume
    print("wait for 10 minutes and increase volume to %s" % (20 * yamaha_system_volume_factor))
    time.sleep((60 * 10))
    requests.get(api_base_url + 'main/setVolume?volume=%s' % (20 * yamaha_system_volume_factor))
    print("volume increased to %s" % (20 * yamaha_system_volume_factor))

    # wait for 10 minutes and stop radio
    print("wait for 10 minutes and stop radio")
    time.sleep((60 * 10))
    requests.get(api_base_url + 'main/setPower?power=standby')


while True:
    wait_till_next_morning()
    # wait_till_given_time(9)

    print("### Ping check to target oauth2.googleapis.com ###")
    os.system("ping -c 1 oauth2.googleapis.com")

    if is_workday():
        play_radio()
