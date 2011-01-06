"""
Models for persistent objects.
"""
from pprint import pprint
import time
import feedparser

from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy initialisation

Base = declarative_base()
engine = create_engine('sqlite:///data/ring.db')
Session = sessionmaker(bind=engine)

# Abstract base class

class Entry(Base):
    __tablename__ = "entry"

    id = Column(String, primary_key=True)
    source = Column(String)
    link = Column(String)
    author = Column(String)
    title = Column(String)
    content = Column(String)

    published = Column(Integer)
    updated = Column(Integer)

    new_date = None

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)



class Feed(Base):
    __tablename__ = "feed"

    id = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    url = Column(String)
    home_url = Column(String)

    author = ""
    

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def crawl(self):
        session = Session()
        raw_feed = feedparser.parse(self.url)
        print raw_feed.keys()

        self.url = raw_feed.href
        self.home_url = raw_feed.feed.link
        self.title = raw_feed.feed.title
        for raw_entry in raw_feed.entries:
            id = raw_entry.id
            if session.query(Entry.id).filter(Entry.id==id).all():
                continue
            #pprint(raw_entry)
            e = raw_entry

            author = e.get('author', self.author)

            if e.has_key('content'):
                content = e.content[0].value
            else:
                content = e.summary

            if e.has_key('published_parsed'):
                published = time.mktime(e.published_parsed)
            else:
                published = 0
            if e.has_key('updated_parsed'):
                updated = time.mktime(e.updated_parsed)
            else:
                updated = 0
            if not updated:
                updated = published
            if not published:
                published = updated
            entry = Entry(id=id, source=self.id, link=e.link, author=author, title=e.title,
                          content=content, published=published, updated=updated)
            session.add(entry)
        session.commit()

Base.metadata.create_all(engine)
