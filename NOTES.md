Goals for the Ring project
===============================

Features
--------

- "Better planet than planetplanet"

Why better?

- Uses a "standard" templating engine (ex: Jinja)
- Archives
- Filters <- killer feature for me

But still:

- Hype-easy to deploy

Architecture
------------

Here is a list of technical requirements / architecture specs:

- Use Flask
- Databased-backed (start with sqlite, but should be DB-independent)
- Dynamic + static site generation
- Uses feeparser
- But also able to do screen-scrapping
- Knows how to "fix" bad HTML content
- Has unit tests
- 1-line deploy using Fabric
- 2 main processes communicating by sharing the database:
  - 1 server (serves web pages)
  - 1 crawler (crawls feeds)
