import json

settings = None
mapping = None
unwantedcourses = None
settingsfilename = 'settings.json'
mappingfilename = 'mapping.json'

def loadConfig():
  global settings, mapping, unwantedcourses
  with open(settingsfilename, 'r') as infile:
    settings = json.load(infile)
  with open(mappingfilename, 'r') as infile:
    mapping = json.load(infile)
  unwantedcourses = []
  for key, value in mapping.items():
    if value['ignore']:
      unwantedcourses.append(key)

def getName(originalname, courseid):
  global mapping
  inputvalue = mapping.get(courseid)
  if inputvalue is not None:
    return inputvalue['name']
  name = "U' " + originalname
  mapping[courseid] = {
    'name': name,
    'ignore': False
  }
  updateMapping()
  return name

def updateMapping():
  global mapping
  with open(mappingfilename, 'w') as outfile:
    json.dump(mapping, outfile, indent=2, sort_keys=False)

