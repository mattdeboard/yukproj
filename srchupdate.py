import os
import subprocess
import sys
import logging

domain_dir = "/a/mattdeboard.net/"
appdir = domain_dir + "src/yukproj/"
whoosh_dir = appdir + "yuk/whoosh/"

def update():
    logging.basicConfig(filename='/a/mattdeboard.net/src/index.log', 
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s', 
                        datefmt='%m/%d/%Y %H:%M:%S')
    logging.info('Starting index update.')
    try:
        mattwhoosh = subprocess.call(['sudo', 'chown', '-R',
                                      'matt:matt', whoosh_dir])
        update_index = subprocess.call([domain_dir+'bin/python', 
                                        appdir+'manage.py', 'update_index'])
        apachewhsh = subprocess.call(['sudo', 'chown', '-R',
                                      'www-data:www-data', whoosh_dir])
        apachereload = subprocess.call(['sudo', 
                                        '/etc/init.d/apache2', 'force-reload'])
        if sum([int(mattwhoosh), int(update_index), int(apachewhsh), 
                int(apachereload)]) == 0:
            logging.info('Index successfully updated.')
            logging.error('The following exit codes were returned:')
            logging.error('- mattwhoosh: %s' % mattwhoosh)
            logging.error('- update_index: %s' % update_index)
            logging.error('- apachewhsh: %s' % apachewhsh)
            logging.error('- apachereload: %s' % apachereload)
        else:
            logging.error('**INDEX UPDATE FAILED**')
            logging.error('The following exit codes were returned:')
            logging.error('- mattwhoosh: %s' % mattwhoosh)
            logging.error('- update_index: %s' % update_index)
            logging.error('- apachewhsh: %s' % apachewhsh)
            logging.error('- apachereload: %s' % apachereload)
    except:
        logging.error("Exception received: ", 
                      sys.exc_info()[0], 
                      sys.exc_info()[1])


if __name__ == '__main__':
    update()

