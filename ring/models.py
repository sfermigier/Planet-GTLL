"""
Models for persistent objects.
"""

import time
import feedparser
import os

from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# TODO: move to config.
ENGINE = "sqlite:///data/ring.db"

# SQLAlchemy initialisation

Base = declarative_base()
if ENGINE.startswith("sqlite:///data/") and not os.path.exists("data"):
    os.mkdir("data")
engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)


class Entry(Base):
    __tablename__ = "entry"

    id = Column(String, primary_key=True)
    source = Column(String)
    link = Column(String)
    author = Column(String)
    author_email = Column(String)
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

    # TODO:move to crawler.
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

            author_email = e.get("author_detail", {}).get("email", "")
                
            entry = Entry(id=id, source=self.id, link=e.link, author=author, title=e.title,
                          content=content, published=published, updated=updated,
                          author_email=author_email)
            session.add(entry)
        session.commit()

Base.metadata.create_all(engine)
