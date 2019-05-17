from urllib.request import urlopen
import config
import os

def getCalendar():
  debugmode = os.environ['ENV'] == 'dev'
  if debugmode:
    return readCalendarFile()
  else:
    return readCalendarFeed()

def readCalendarFeed():
  url = config.settings['feed']
  print('Requesting new calendar from moodle...')
  return urlopen(url).read().decode('utf8')

def readCalendarFile():
  filename = 'icslexport.ics'
  if not os.path.isfile(filename):
    content = readCalendarFeed()
    file = open(filename, mode='w', encoding="utf8")
    file.write(content)
    file.close()
  else: 
    content = open('icslexport.ics', encoding="utf8").read()
  return content
