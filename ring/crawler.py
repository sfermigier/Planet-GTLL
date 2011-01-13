"""Crawler for ring.

Responsible for
"""
import config, models

class Crawler(object):

    def __init__(self):
        self.feeds = []
        cfg = config.config()
        for section in cfg.sections():
            if section == "META":
                continue
            d = {}
            d.update(cfg.items(section))
            print d
            if d.has_key("crawler"):
                feed = getattr(models, d['crawler'])(id=section, **d)
            else:
                feed = models.Feed(id=section, **d)
            self.feeds.append(feed)

    def crawl(self):
        for source in self.feeds:
            print "Crawling", source
            source.crawl()

def main():
    crawler = Crawler()
    crawler.crawl()

if __name__ == '__main__':
    main()
