import json

settings = None
mapping = None
unwantedcourses = None
settingsfilename = 'settings.json'
mappingfilename = 'mapping.json'
mappingUpdated = False

def loadConfig():
  global settings, mapping, unwantedcourses, mappingUpdated
  with open(settingsfilename, 'r') as infile:
    settings = json.load(infile)
    infile.close()
  with open(mappingfilename, 'r') as infile:
    mapping = json.load(infile)
    infile.close()
  unwantedcourses = []
  for key, value in mapping.items():
    if value['ignore']:
      unwantedcourses.append(key)
  mappingUpdated = False

def getName(courseid):
  global mapping
  element = mapping.get(courseid)
  if element is not None:
    return element['name']
  return element

def storeName(originalname, courseid):
  global mapping, mappingUpdated
  name = "U' " + originalname
  mapping[courseid] = {
    'name': name,
    'ignore': False
  }
  mappingUpdated = True
  return name

def updateMapping():
  global mapping, mappingUpdated
  if not mappingUpdated:
    return
  with open(mappingfilename, 'w') as outfile:
    json.dump(mapping, outfile, indent=2, sort_keys=True)

