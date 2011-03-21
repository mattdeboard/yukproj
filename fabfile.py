from calendar import timegm
from time import gmtime

from fabric.api import *
from hosts import hosts

env.hosts = hosts
domain_dir = "/a/mattdeboard.net/"
appdir = domain_dir + "src/yukproj/"
# directory where git puts the css files on git pull
css_dir = appdir + "yuk/static/css/blueprint/"
# where nginx looks for static files
static_file_dir = domain_dir + "root/yukmarks/css/blueprint/"
pg_dump_dir = domain_dir + "pg_dumps/"
whoosh_dir = appdir + "yuk/whoosh/"

def git_pull():
    run("cd %s; . bin/activate; cd %s; git pull; ./manage.py schemamigration"
        " --auto yuk; ./manage.py migrate yuk;cp %s* %s;sudo /etc/init.d/apache2"
        " force-reload" % (domain_dir, appdir, css_dir, static_file_dir))

def pg_dump():
    timestamp = timegm(gmtime())
    run("cd %s; . bin/activate; cd %s; pg_dump -f %spg_dump_%s.sql pg_links" % 
        (domain_dir, appdir, pg_dump_dir, timestamp))

def dump_data():
    timestamp = timegm(gmtime())
    run("cd %s; . bin/activate; cd %s; ./manage.py dumpdata --format=json yuk"
        " >> /a/mattdeboard.net/yuk_data_dumps/dump_%s.json" % 
        (domain_dir, appdir, timestamp))

def update_search():
    run("cd %s; . bin/activate; cd %s; sudo chown matt:matt %s; sudo chown matt"
        ":matt %s*; ./manage.py update_index; sudo chown www-data:www-data %s; "
        "sudo chown www-data:www-data %s*; sudo /etc/init.d/apache2 force-reloa"
        "d" % (domain_dir, appdir, whoosh_dir, 
               whoosh_dir, whoosh_dir, whoosh_dir))

def rebuild_search():
    run("cd %s; . bin/activate; cd %s; sudo chown matt:matt %s; sudo chown matt"
        ":matt %s*; ./manage.py rebuild_index; sudo chown www-data:www-data %s;"
        " sudo chown www-data:www-data %s*; sudo /etc/init.d/apache2 force-relo"
        "ad" % (domain_dir, appdir, whoosh_dir, 
               whoosh_dir, whoosh_dir, whoosh_dir))
