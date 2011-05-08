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
    update_index = subprocess.Popen(['sudo', '-u', 'www-data', 
                                   domain_dir+'bin/python',
                                   appdir+'manage.py', 'update_index'],
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT)
    update_index.wait()
    apachereload = subprocess.Popen(['sudo', 
                                     '/etc/init.d/apache2', 
                                     'force-reload'],
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.STDOUT)
    apachereload.wait()
    if not any((update_index.returncode, apachereload.returncode)):
        logging.info('Index successfully updated.')
    else:
        subs = [update_index, apachereload]
        logging.error('**INDEX UPDATE FAILED**')
        logging.error('The following exit codes were returned:')
        logging.error('- update_index: %s' % update_index.returncode)
        logging.error('- apachereload: %s' % apachereload.returncode)
        for sub in subs:
            if sub.returncode:
                logging.error('Error information:')
                logging.error('stdout: %s' % sub.communicate()[0])
                logging.error('stderr: %s' % sub.communicate()[1])


if __name__ == '__main__':
    update()

