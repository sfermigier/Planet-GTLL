from cgi import escape
import time, re
from urllib import quote
import feedparser

from models import Event, Source

# Patch feedparser. Yuck :(
feedparser._HTMLSanitizer.acceptable_elements += ['style']

#
# RSS / Atom Feed abstract class
#

class Feed(Source):
    """Abstract base class: do not instantiate."""

    feed_url = None

    def crawl(self):
        d = feedparser.parse(self.feed_url)
        self.source_url = d.href
        self.home_url = d.feed.link
        self.title = d.feed.title
        entries = d.entries

        events = [ self.make_event(entry) for entry in entries ]

        # TODO: refactor
        for event in events:
            if not self.session.query(Event.uid).filter(Event.uid==event.uid).all():
                self.session.add(event)
        self.session.commit()


    def make_event(self, entry):
        event = Event()
        event.type = self.type
        event.title = entry.title
        event.uid = entry.id
        event.url = entry.link
        event.created = time.mktime(entry.updated_parsed)
        event.author = entry.get("author", "unknown")
        if entry.has_key("content"):
            event.content = entry.content[0].value
        elif entry.has_key("summary"):
            event.content = entry.summary
        else:
            event.content = ""
        self.post_init(event, entry)
        return event

    def post_init(self, event, entry):
        pass

#
# Instantiable sources
#

BLOG_AUTHORS = {
    "Stefane Fermigier": "Stefane Fermigier",
    "CherylMcKinnon": "Cheryl McKinnon",
    "Nuxeo": "Nuxeo Team",
    "eric's blog": "Eric Barroca",
    "My job things": "Roland Benedetti",
    "Sun Seng David TAN": "Sun Tan",
}

class Blogs(Feed):
    type = "blogpost"
    feed_url = "http://blogs.nuxeo.com/atom.xml"

    def get_header(self, event):
        return 'New blog post, by <a href="/user/%s">%s</a>' % (
            quote(event.author), escape(event.author))

#

class CorpNews(Feed):
    type = "news"
    feed_url = "http://www.nuxeo.com/nxc/rssfeed/news"

    def post_init(self, event, entry):
        event.author = "Nuxeo Corp"

    def get_header(self, event):
        return "New Corporate announcement, on <a href='http://www.nuxeo.com/'>nuxeo.com</a>"

#

class Buzz(Feed):
    type = "buzz"
    feed_url = "http://www.nuxeo.com/en/rss/feed/buzz"

    def post_init(self, event, entry):
        event.author = "Nuxeo Corp"

    def get_header(self, event):
        return "Buzz about us, displayed on <a href='http://www.nuxeo.com/'>nuxeo.com</a>"

#

class Forum(Feed):
    type = "forum"
    feed_url = "http://forum.nuxeo.org/feed.php?mode=m&l=1&basic=1"

    def post_init(self, event, entry):
        m = re.match(r"http://forum.nuxeo.org/\./mv/msg/([0-9]+)/([0-9]+)", event.url)
        tid = int(m.group(1))
        mid = int(m.group(2))
        event.url = "http://forum.nuxeo.org/?t=msg&th=%d&goto=%d&#msg_%d" % (tid, mid, mid)

    def get_header(self, event):
        if event.title.startswith("Re:"):
            return 'New reply on the forum, by <a href="/user/%s">%s</a>' % (
                quote(event.author), escape(event.author))
        else:
            return 'New thread on the forum, by <a href="/user/%s">%s</a>' % (
                quote(event.author), escape(event.author))

#

class Documentation(Feed):
    type = "documentation"
    feed_url = "https://doc.nuxeo.com/spaces/createrssfeed.action?spaces=conf_all" + \
        "&types=page&types=comment&types=blogpost&types=mail&types=attachment" + \
        "&maxResults=15&publicFeed=true"

    def get_header(self, event):
        return 'Documentation change, by <a href="/user/%s">%s</a>' % (
            quote(event.author), escape(event.author))

#

class Jira(Feed):
    type = "jira"
    feed_url = "http://jira.nuxeo.org/sr/jira.issueviews:searchrequest-rss/10915/SearchRequest-10915.xml?tempMax=10"

    def post_init(self, event, entry):
        m = re.search(r"Created: (.*?)\s*&nbsp;Updated: ([^\s]*)", event.content)
        if m:
            created = m.group(1)
            updated = m.group(2)
            if created == updated:
                event.subtype = "new"
            else:
                event.subtype = "update"
        else:
            event.subtype = "update"

    def get_header(self, event):
        if event.subtype == 'new':
            return 'New Jira issue, by <a href="/user/%s">%s</a>' % (
                quote(event.author), escape(event.author))
        else:
            return 'Jira issue update, by <a href="/user/%s">%s</a>' % (
                quote(event.author), escape(event.author))

#############################################################################

# Poor man's plugin registration

all_sources = [Blogs(), Forum(), CorpNews(), Buzz(), Jira(), Documentation()]

def get_header_for(event):
    type = event.type.split("/")[0]
    for source in all_sources:
        if source.type == type:
            return source.get_header(event)
    raise "Unknown source"
