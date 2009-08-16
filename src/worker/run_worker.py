import os
import urllib2
import simplejson
import tarfile
import time
import logging

from worker import settings
from worker import Worker
from worker import daemon

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a",
                      "--action",
                      dest="action",
                      help="Action can be : start|stop|restart",
                      default=""
                      )    
    parser.add_option("-k",
                      "--kitchen",
                      dest="kitchen",
                      help="Kitchen used to cook the recipe",
                      default=settings.WORKER_KITCHEN
                      )
    parser.add_option("-i",
                      "--interval",
                      dest="interval",
                      help="interval between each check",
                      default=settings.WORKER_INTERVAL
                      )
    parser.add_option("-f",
                      "--factory_url",
                      dest="factory_url",
                      help="Url of the fabric factory",
                      default=settings.FABRIC_FACTORY_URL
                      )
    parser.add_option("-b",
                      "--keep_builds",
                      dest="keep_builds",
                      help="keep files used to make the build",
                      default=settings.WORKER_KEEP_BUILDS
                      )
    (options, args) = parser.parse_args()
    logging.debug('command line options : %s' %options)
    pid_file = os.path.join(os.getcwd(),'worker_daemon.pid' )
    worker_daemon = WorkerDaemon(pid_file)
    if options.action == "start":
        worker_daemon.start(options)
    elif options.action == "stop":
        worker_daemon.stop()
    elif options.action == "restart":
        worker_daemon.restart()
    else:
        worker = worker_factory(factory_url=options.factory_url,
                       kitchen_path=options.kitchen)
        if worker is not None:
            logging.debug("worker download the build package")
            worker.download_build_package()
            logging.debug("Worker execute the task")
            worker.execute_task()
            logging.debug("Worker post the result")
            worker.post_result()
            if not options.keep_builds:
                logging.debug("Worker clean the kitchen after the build")
                worker.clean()
    


def worker_factory(factory_url, kitchen_path):
    response = urllib2.urlopen(factory_url, data=None)
    json = response.read()
    logging.debug('json response from the factory server \n %s' %json)
    worker_dict = simplejson.loads(json)
   
    if worker_dict:
        worker = Worker(name=worker_dict['name'], task=worker_dict['task'],
                    post_back_url=worker_dict['post_back_url'],
                    build_package_url=worker_dict['build_package_url'],
                    kitchen_path=kitchen_path)
        return worker
    else:
        return None

    
class WorkerDaemon(daemon.Daemon):
    def run(self, options):
        while True:
            logging.debug("Worker search for a gig")
            time.sleep(options.interval)
            worker = worker_factory(factory_url=options.factory_url,
                           kitchen_path=options.kitchen)
            if worker is not None:
                logging.debug("worker download the build package")
                worker.download_build_package()
                logging.debug("Worker execute the task")
                worker.execute_task()
                logging.debug("Worker post the result")
                worker.post_result()
                if not options.keep_builds:
                    logging.debug("Worker clean the kitchen after the build")
                    worker.clean()


if __name__ == '__main__':
    main()
    