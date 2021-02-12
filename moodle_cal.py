from urllib.request import urlopen
import config
import os
import datetime


def get_calendar():
    debugmode = os.environ["ENV"] == "dev"
    if debugmode:
        return read_calendar_file()
    else:
        return read_calendar_feed()


def read_calendar_feed():
    url = config.settings["feed"]
    print("Requesting new calendar from moodle...")
    return urlopen(url).read().decode("utf8")


def read_calendar_file():
    filename = "icslexport.ics"
    if not os.path.isfile(filename):
        content = read_calendar_feed()
        file = open(filename, mode="w", encoding="utf8")
        file.write(content)
        file.close()
    else:
        content = open("icslexport.ics", encoding="utf8").read()
    return content
