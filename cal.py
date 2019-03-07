import re
import config
import moodle_cal


def getModifiedCalendar():
  return 'TODO'



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