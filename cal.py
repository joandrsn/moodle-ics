import re
import config
import moodle_cal
from ics import Calendar
import datetime


def get_modified_calendar():
    config.load_config()
    calendar = Calendar(moodle_cal.get_calendar())
    remove_unwanted_events(calendar)
    update_events(calendar.events)
    config.update_mapping()
    return str(calendar)


def remove_unwanted_events(calendar):
    calendar.events = [e for e in calendar.events if not should_remove_event(e)]


def should_remove_event(event):
    startmonth = event.begin.month
    if not startmonth in config.settings["ignoremonths"]:
        return False
    courseid = get_course_id(event.categories)
    if courseid == None:
        return False
    return courseid in config.unwantedcourses


def update_events(events):
    for event in events:
        courseid = get_course_id(event.categories)
        originalname = event.name
        if courseid == "":
            continue
        event.name = get_new_name(originalname, courseid)
        event.url = get_new_url(courseid)
        if not originalname.startswith("Course:"):
            continue
        namedict = parse_event_summary(originalname)

        event.description = get_new_description(
            event.description, namedict.get("Note"), namedict.get("Teacher")
        )
        event.location = get_new_location(event.location, namedict.get("Place"))


def get_course_id(categories):
    for category in categories:
        break
    regex = r"\[([FE]\d{2}-\d{5,})\]$"
    idmatch = re.search(regex, category)
    if idmatch == None:
        return ""
    return idmatch.group(1)


def parse_event_summary(eventsummary):
    regex = r"([A-Za-z]+): (.+?)(?= - [A-Z]|$)"
    objdict = {}
    listmatch = re.findall(regex, eventsummary)
    if listmatch == None:
        return None
    for element in listmatch:
        objdict[element[0]] = element[1]
    return objdict


def get_new_description(originaleventdescription, note, teacher):
    array = []
    if note != None:
        array.append(note)
    if teacher != None:
        array.append(teacher)
    if originaleventdescription != None:
        array.append(originaleventdescription)
    return str.join("\n", array)


def get_new_location(orignallocation, newlocation):
    if newlocation == None:
        return orignallocation
    return newlocation


def get_new_name(originalname, courseid):
    shortname = config.get_name(courseid)

    if courseid != "":
        config.store_name(originalname, courseid)

    if shortname is not None:
        return shortname
    else:
        return originalname


def get_new_url(courseid):
    match = re.search(r"\d+$", courseid)
    return config.settings["baseurl"] + match.group()
