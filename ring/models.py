# -*- coding: UTF8 -*-

"""
Models for persistent objects.
"""

import time
import urllib
import feedparser
import lxml.html
import os
import re

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

    def __repr__(self):
        return "<Feed id=%s>" % self.id

    # TODO:move to crawler.
    def crawl(self):
        session = Session()
        raw_feed = feedparser.parse(self.url)

        self.url = raw_feed.href
        self.home_url = raw_feed.feed.link
        self.title = raw_feed.feed.title
        for raw_entry in raw_feed.entries:
            id = raw_entry.get('id', raw_entry.link)
            if session.query(Entry.id).filter(Entry.id==id).all():
                continue
            e = raw_entry

            author = e.get('author', self.author)

            if e.has_key('content'):
                content = e.content[0].value
            elif e.has_key('summary'):
                content = e.summary
            else:
                content = ""

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

class GtllFeed(Feed):
    ROOT = "http://www.systematic-paris-region.org/"
    HOME = ROOT + "fr/news/actualites/logiciel-libre"
    PAT1 = '<span class="field-content"><a href="(/fr/actualites/[a-z-]*?)">(.*?)</a></span>'

    # TODO:move to crawler.
    def crawl(self):
        session = Session()

        self.url = self.HOME
        self.home_url = self.HOME

        self.title = "Actualités du GTLL"

        root_page = urllib.urlopen(self.HOME).read()
        matches = re.findall(self.PAT1, root_page)

        for slug, title in matches:
            id = slug
            if session.query(Entry.id).filter(Entry.id==id).all():
                continue

            link = self.ROOT + slug
            page = urllib.urlopen(link).read()
            tree = lxml.html.fromstring(page)
            elems = tree.xpath("//div[@class='node-inner']/div[@class='content']/*")

            content = ""
            for e in elems[1:]:
                fragment = lxml.html.tostring(e).strip()
                content += fragment

            content = re.sub(r'<a href="/(.*?)">', '<a href="%s/\1">' % self.ROOT, content)

            author = "Unknown"

            s = tree.xpath("//div[@class='submitted']/text()")[0].strip()
            published = time.mktime((int(s[6:10]), int(s[3:5]), int(s[0:2]), 0, 0, 0, 0, 0, 0))
            updated = published

            author_email = ""

            title = title.decode("utf8")
            content = content.decode("utf8")
            entry = Entry(id=id, source=self.id, link=link, author=author, title=title,
                          content=content, published=published, updated=updated,
                          author_email=author_email)
            session.add(entry)

        session.commit()


Base.metadata.create_all(engine)
