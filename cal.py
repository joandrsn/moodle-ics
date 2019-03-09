import re
import config
import moodle_cal
from ics import Calendar


def getModifiedCalendar():
  config.loadConfig()
  calendar = Calendar(moodle_cal.getCalendar())
  updateEvents(calendar.events)
  return len(calendar.events)


def updateEvents(events):
  for event in events:
    if not event.name.startswith('Course:'):
      continue
    courseid = getCourseID(event.categories)
    namedict = parseEventSummary(event.name)

    event.description = getNewDescription(event.description, namedict.get('Note'), namedict.get('Teacher'))
    event.location = getNewLocation(event.location, namedict.get('Place'))
    oldname = event.name
    #print(oldname)
    event.name = getNewName(event.name, courseid)
    #print(' AFTER:' + event.name + ' BEFORE: ' + oldname)
    print(event.name)

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
  return config.getName(originalname, courseid)