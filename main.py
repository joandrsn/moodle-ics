from flask import Flask, Response, request
from ics import Calendar
import re
app = Flask(__name__)

@app.route('/calendar.ics')
def getCalendar():
  key = request.args.get('key')
  if key != 'dDH4oFhogjcFRigxGtdf':
    return Response('Unauthorized', 401)
  calObj = readCalendarFile()
  calObj.events = [e for e in calObj.events if not shouldEventBeRemoved(e)] #Remove unwanted elements by using list comprehesion
  for event in calObj.events:
    convertNameDescription(event)
  return Response(
    str(calObj),
    mimetype='text/calendar',
    headers={"Content-Disposition":
      "attachment; filename=calendar.ics"})

def readCalendarFile():
  calfile = open('icslexport.ics', encoding="utf8")
  return Calendar(calfile.read())

def shouldEventBeRemoved(event):
  startmonth = event.begin.month
  if startmonth in [1, 2, 6, 7, 8, 9]:
    return False
  identifier = getIdentifier(event)
  if identifier == None:
    return False
  return identifier in ['F19-28470', 'F19-28487', 'F19-28405']

def convertNameDescription(event):
  if not event.name.startswith("Course:"):
    return
  splitorigname = re.split(r' - ([a-zA-Z]+): ', event.name)
  setLocation(event, splitorigname)
  setName(event, splitorigname[0])
  setTeacher(event, splitorigname)
  setNote(event, splitorigname)

def setLocation(event, splitarray):
  try:
    placeindex = splitarray.index("Place")
  except ValueError:
    placeindex = -1
  if placeindex != -1:
    event.location = splitarray[placeindex + 1]

def setName(event, fallback):
  identifier = getIdentifier(event)
  if identifier == None:
    return
  convertedName = convertName(identifier)
  if convertedName == "":
    convertedName = "U' " + fallback
  event.name = convertedName

def getIdentifier(event):
  firstcategory = getFirstCategory(event)
  moodleid = re.search(r'\[([FE]\d{2}-\d{5})\]$', firstcategory)
  if not moodleid:
    return None
  return moodleid.group(1)

def setNote(event, splitarray):
  placeindex = findIndex(splitarray, "Note")
  if placeindex != -1:
    olddescription = event.description
    event.description = "Note:" + splitarray[placeindex + 1]
    if olddescription != "":
      event.description = event.description + "\n" + olddescription

def setTeacher(event, splitarray):
  placeindex = findIndex(splitarray, "Teacher")
  if placeindex != -1:
    olddescription = event.description
    event.description = "Teacher:" + splitarray[placeindex + 1]
    if olddescription != "":
      event.description = event.description + "\n" + olddescription

def convertName(key):
  result = ""
  if key == 'F19-28774':
    result = "SPO"
  elif key == 'F19-28773':
    result = "PSS"
  elif key == 'F19-28497':
    result = "SLIAL"
  elif key == 'F19-28797':
    result = "Software 4"
  elif key == 'F19-28356':
    result = "Helligdag"
  elif key == 'F19-28358':
    result = "Projekt aflevering maj 2019"
  elif key == 'F19-28499':
    result = "Studiecafe for IT-uddannelser"
  elif key == 'F19-28781':
    result = 'SS'
  return result

def getFirstCategory(event):
  for firstcategory in event.categories: break
  return firstcategory

def findIndex(array, element):
  try:
    return array.index(element)
  except ValueError:
    return -1

if __name__ == '__main__':
    app.run(debug=True)
