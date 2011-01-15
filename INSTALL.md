How to install?
===============

## Install virtualenv and pip

Mac:

    $ port install py26-virtualenv py26-pip

Linux:

    $ apt-get install python-virtualenv python-pip

Etc.

## Install the app

Type:

$ make

## Run

a) Start the server with:

    $ make serve

b) Crawl the feed with:

    $ ./ring.sh crawl

(You might want to set up a crontab).
  
## Configure

Edit `ring.cfg`
