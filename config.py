import json

settings = None
mapping = None
settingsfilename = 'settings.json'
mappingfilename = 'mapping.json'

def loadConfig():
  global settings, configfilename, mapping, mappingfilename
  with open(configfilename, 'r') as infile:
    settings = json.load(infile)
  with open(mappingfilename, 'r') as infile:
    mapping = json.load(infile)

def getName(originalname, courseid):
  global mapping
  inputvalue = mapping.get(courseid)
  if inputvalue is not None:
    return inputvalue
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

