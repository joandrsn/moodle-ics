from urllib.request import urlopen
import config

def getCalendar():
  FILE_MODE = False
  if FILE_MODE:
    return readCalendarFile()
  else:
    return readCalendarFeed()

def readCalendarFeed():
  url = config.settings['feed']
  print('Requesting new calendar from moodle...')
  return urlopen(url).read().decode('utf8')

def readCalendarFile():
  calfile = open('icslexport.ics', encoding="utf8")
  return calfile.read()
