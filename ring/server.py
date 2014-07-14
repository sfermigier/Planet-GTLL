#!env/bin/python
# -*- coding: UTF8 -*-


import time
import datetime

from flask import *
from werkzeug.contrib.atom import AtomFeed

from models import Entry, Session
from config import config

CFG = config()

# Constants
MAX_ENTRIES = 12

# Real constants
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
MONTH = 30 * DAY
YEAR = 365 * DAY

BLOG = {
    'url': 'http://www.gt-logiciel-libre.org/',
    'title': u"Planète GTLL",
    'tagline': u"Échos de l'écosystème du libre en Ile-de-France",
    'menu': [{'url': "", 'title': 'Home'},
             #{'url': "about", 'title': 'About'},
             #{'url': "category/public-speaking", 'title': 'Public Speaking'},
    ]
}

try:
    import newrelic.agent
    import os
    here = os.path.dirname(__file__)
    newrelic.agent.initialize(os.path.join(here, '..', 'newrelic.ini'))
except:
    import traceback
    traceback.print_exc()
    pass

# Use /media instead of default /static because /static is already used.
app = Flask(__name__, static_path='/media')
app.jinja_loader.searchpath = ['./templates'] + app.jinja_loader.searchpath

@app.before_request
def connect_db():
    g.session = Session()
    g.age = age

# REST endpoints

@app.route('/')
def home():
    entries = get_entries()
    new_dates = get_new_dates(entries)
    model = dict(entries=entries, new_dates=new_dates, blog=BLOG)
    response = make_response(render_template("home.html", **model))
    return response


@app.route('/rss')
def feed():
    feed = AtomFeed(BLOG['title'], url=BLOG['url'], feed_url=request.url,
                    subtitle=BLOG['tagline'])
    for e in get_entries():
        title = "[%s] %s" % (e.source, e.title)
        feed.add(title=title, content=e.content, content_type='text/html',
                 author=e.author, url=e.link, id=e.id,
                 updated=datetime.datetime.utcfromtimestamp(e.updated),
                 published=datetime.datetime.utcfromtimestamp(e.published))
    return feed.get_response()

# Debug
@app.route('/rss-debug')
def feed_debug():
    return feed()

# Utility functions

def get_entries():
    query = g.session.query(Entry)
    entries = query.order_by(Entry.published.desc()).limit(MAX_ENTRIES)

    return entries


def get_new_dates(entries):
    d = {}
    for entry in entries:
        date = time.localtime(entry.published)[0:3]
        d[date] = d.get(date, ()) + (entry,)

    l = d.items()
    l.sort(lambda x, y: -cmp(x[0], y[0]))
    new_dates = {}
    for date, l1 in l:
        new_dates[l1[0]] = datetime.date(*date)
    return new_dates


def age(t):
    now = int(time.time())
    dt = now - t
    if dt < MINUTE:
        return "%d seconds ago" % dt
    if dt < 2 * MINUTE:
        return "about 1 minute ago"
    if dt < HOUR:
        return "%d minutes ago" % (dt / MINUTE)
    if dt < 2 * HOUR:
        return "about 1 hour ago"
    if dt < DAY:
        return "about %d hours ago" % (dt / HOUR)
    if dt < 2 * DAY:
        return "yesterday"
    if dt < MONTH:
        return "about %d days ago" % (dt / DAY)
    if dt < 2 * MONTH:
        return "last month"
    if dt < YEAR:
        return "about %d months ago" % (dt / MONTH)
    return "%d years ago" % (dt / YEAR)


def main():
    app.run(debug=True, port=5200)

if __name__ == '__main__':
    main()
