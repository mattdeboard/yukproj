from calendar import timegm
from time import gmtime

from fabric.api import *
from hosts import hosts

env.hosts = hosts

def git_pull():
    run("cd /a/mattdeboard.net; . bin/activate; cd src/yukproj; git pull; ./manage.py schemamigration --auto yuk; ./manage.py migrate yuk; sudo /etc/init.d/apache2 force-reload")

def pg_dump():
    timestamp = timegm(gmtime())
    run("cd /a/mattdeboard.net; . bin/activate; cd src/yukproj; pg_dump -f /a/mattdeboard.net/pg_dumps/pg_dump_%s" % timestamp)

def dump_data():
    timestamp = timegm(gmtime())
    run("cd /a/mattdeboard.net; . bin/activate; cd src/yukproj; ./manage.py dumpdata --format=json yuk >> /a/mattdeboard.net/yuk_data_dumps/dump_%s" % timestamp)

def update_search():
    run("cd /a/mattdeboard.net; . bin/activate; cd src/yukproj; sudo chown matt:matt yuk/whoosh; sudo chown matt:matt yuk/whoosh/*; ./manage.py update_index; sudo chown www-data:www-data yuk/whoosh; sudo chown www-data:www-data yuk/whoosh/*; sudo /etc/init.d/apache2 force-reload")
