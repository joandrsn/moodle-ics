import re
import config
import moodle_cal
from ics import Calendar


def getModifiedCalendar():
  config.loadConfig()
  calendar = Calendar(moodle_cal.getCalendar())
  removeUnwantedEvents(calendar)
  updateEvents(calendar.events)
  return str(calendar)

def removeUnwantedEvents(calendar):
  calendar.events = [e for e in calendar.events if not shouldEventBeRemoved(e)]
  

def shouldEventBeRemoved(event):
  startmonth = event.begin.month
  if not startmonth in config.settings['ignoremonths']:
    return False
  courseid = getCourseID(event.categories)
  if courseid == None:
    return False
  return courseid in config.unwantedcourses

def updateEvents(events):
  for event in events:
    courseid = getCourseID(event.categories)
    originalname = event.name
    event.name = getNewName(originalname, courseid)
    event.url = getNewURL(courseid)
    if not originalname.startswith('Course:'):
      continue
    namedict = parseEventSummary(originalname)

    event.description = getNewDescription(event.description, namedict.get('Note'), namedict.get('Teacher'))
    event.location = getNewLocation(event.location, namedict.get('Place'))

def getCourseID(categories):
  for category in categories: break
  regex = r'\[([FE]\d{2}-\d{5,})\]$'
  idmatch = re.search(regex, category)
  if idmatch == None:
    return ''
  return idmatch.group(1)

def parseEventSummary(eventsummary):
  regex = r'([A-Za-z]+): (.+?)(?= - [A-Z]|$)'
  objdict = {}
  listmatch = re.findall(regex, eventsummary)
  if listmatch == None:
    return None
  for element in listmatch:
    objdict[element[0]] = element[1]
  return objdict

def getNewDescription(originaleventdescription, note, teacher):
  array = []
  if note != None:
    array.append(note)
  if teacher != None:
    array.append(teacher)
  if originaleventdescription != None:
    array.append(originaleventdescription)
  return str.join("\n", array)

def getNewLocation(orignallocation, newlocation):
  if newlocation == None:
    return orignallocation
  return newlocation

def getNewName(originalname, courseid):
  shortname = config.getName(courseid)
  if originalname.startswith('Course:'):
    if shortname is not None:
      return shortname
    else:
      return config.storeName(originalname, courseid)
  else:
    if shortname is not None:
      return shortname + ": " + originalname
    else:
      return originalname

  searchvalue = originalname
  if not originalname.startswith('Course:'):
    result = ''
  shortname = config.getName(searchvalue, courseid)
  if shortname == '':
    return originalname
  return shortname + ':' + originalname

def getNewURL(courseid):
  match = re.search(r'\d+$', courseid)
  return config.settings['baseurl'] + match.group()