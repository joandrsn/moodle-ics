from flask import Flask, Response, request
from flask_caching import Cache
import cal
import config


cache = Cache(config={"CACHE_TYPE": "simple"})
app = Flask(__name__)
cache.init_app(app)


@cache.cached(timeout=50)
def get_modified_calendar():
    return cal.get_modified_calendar()


@app.route("/calendar.ics")
def get_calendar_file():
    config.load_config()
    key = request.args.get("key")
    if key != config.settings["key"]:
        return Response("Unauthorized", 401)
    return Response(
        get_modified_calendar(),
        mimetype="text/calendar",
        headers={"Content-Disposition": "attachment; filename=calendar.ics"},
    )
