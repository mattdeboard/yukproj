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
        mattwhoosh = subprocess.Popen(['sudo', 'chown', '-R',
                                      'matt:matt', whoosh_dir], 
                                      stdout=subprocess.PIPE, 
                                      stderr=suprocess.STDOUT)
        update_index = subprocess.Popen([domain_dir+'bin/python', 
                                        appdir+'manage.py', 'update_index'],
                                        stdout=subprocess.PIPE, 
                                        stderr=suprocess.STDOUT)
        apachewhsh = subprocess.Popen(['sudo', 'chown', '-R',
                                      'www-data:www-data', whoosh_dir],
                                      stdout=subprocess.PIPE, 
                                      stderr=suprocess.STDOUT)
        apachereload = subprocess.Popen(['sudo', 
                                        '/etc/init.d/apache2', 
                                        'force-reload'],
                                        stdout=subprocess.PIPE, 
                                        stderr=suprocess.STDOUT)
        if sum([int(mattwhoosh), int(update_index), int(apachewhsh), 
                int(apachereload)]) == 0:
            logging.info('Index successfully updated.')
        else:
            subs = [mattwhoosh, update_index, apachewhsh, apachereload]
            logging.error('**INDEX UPDATE FAILED**')
            logging.error('The following exit codes were returned:')
            logging.error('- mattwhoosh: %s' % mattwhoosh)
            logging.error('- update_index: %s' % update_index)
            logging.error('- apachewhsh: %s' % apachewhsh)
            logging.error('- apachereload: %s' % apachereload)
            for sub in subs:
                if sub.returncode:
                    logging.error('Error information:')
                    logging.error('stdout: %s' % sub.communicate()[0])
                    logging.error('stderr: %s' % sub.communicate()[1])

    except:
        logging.error("Exception received: ", 
                      sys.exc_info()[0], 
                      sys.exc_info()[1])


if __name__ == '__main__':
    update()

