from fabric.api import env, run, cd, local, put
import time

env.hosts = ['gtll@oss4cloud.org']

STAGING_DIR = "/var/www/gtll/planet-staging"
PRODUCTION_DIR = "/var/www/gtll/planet-production"

def deploy():
  local("make clean")
  local("rm -f /tmp/planet-gtll.tgz")
  local("tar czf /tmp/planet-gtll.tgz --exclude .git --exclude .tox .")
  put("/tmp/planet-gtll.tgz", "/tmp/")

  run("mkdir -p %s" % STAGING_DIR)
  with cd(STAGING_DIR):
    run("tar zxf /tmp/planet-gtll.tgz")
    run("tox -e py27")

  run("mkdir -p %s" % PRODUCTION_DIR)
  with cd(PRODUCTION_DIR):
    run("sqlite3 data/ring.db .dump > ../backup-data/ring-%d.sql" % int(time.time()))
    run("tar zxf /tmp/planet-gtll.tgz")
    run("if [ ! -e env ]; then virtualenv env; fi")
    run("env/bin/python setup.py develop -U")
    run("circusctl restart planet-gtll")
