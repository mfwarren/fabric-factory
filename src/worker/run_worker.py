import os
import urllib2
import simplejson
import tarfile

from worker import settings
from worker import Worker

def main():
    from optparse import OptionParser
    parser = OptionParser()
    
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
    print options
    worker = worker_factory(factory_url=options.factory_url,
                   kitchen_path=options.kitchen)
    if worker is not None:
        worker.download_build_package()
        worker.execute_task()
        worker.post_result()
        if not options.keep_builds:
            worker.clean()

def worker_factory(factory_url, kitchen_path):
    response = urllib2.urlopen(factory_url, data=None)
    json = response.read()
    worker_dict = simplejson.loads(json)
    if worker_dict:
        worker = Worker(name=worker_dict['name'], task=worker_dict['task'],
                    post_back_url=worker_dict['post_back_url'],
                    build_package_url=worker_dict['build_package_url'],
                    kitchen_path=kitchen_path)
        return worker
    else:
        return None


if __name__ == '__main__':
    main()
    