from flask import Flask, Response, request
from flask_caching import Cache
import cal
import config

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)

@cache.cached(timeout=50)
def getModifiedCalendar():
  return cal.getModifiedCalendar()

@app.route('/calendar.ics')
def getCalendarFile():
  config.loadConfig()
  key = request.args.get('key')
  if key != config.settings['key']:
    return Response('Unauthorized', 401)
  return Response(
    getModifiedCalendar(),
    mimetype='text/calendar',
    headers={"Content-Disposition":
      "attachment; filename=calendar.ics"})
