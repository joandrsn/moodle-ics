import json

config = None

def loadConfig():
  global config
  with open('config.json', 'r') as infile:
    config = json.load(infile)

def getName(originalname, courseid):
  global config
  inputvalue = config['COURSEMAPPING'].get(courseid)
  if inputvalue is not None:
    return inputvalue
  name = "U' " + originalname
  config['COURSEMAPPING'][courseid] = {
    'name': name,
    'ignore': False
  }
  updateConfig()
  return name

def updateConfig():
  global config
  with open('config2.json', 'w') as outfile:
    json.dump(config, outfile, indent=2, sort_keys=False)

