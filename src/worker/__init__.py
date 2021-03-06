from glob import glob
from imp import load_source
from shutil import rmtree
from StringIO import StringIO
import logging
import os
import sys
import tarfile
import urllib
import urllib2


from worker import settings

class WorkerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)



class Worker(object):
    def __init__(self, name, task, post_back_url, build_package_url,
                 kitchen_path):
        self.name = name
        self.post_back_url = post_back_url
        self.build_package_url = build_package_url
        self.kitchen_path = kitchen_path
        self.filename = None
        self.task = task 
        self.executed = False
        self.success = False
        self.revision = None
        self.output = None
        self.error = None
    def download_build_package(self):
        logging.debug("try to download the build package : %s" %
                      self.build_package_url)
        if not os.path.isdir(self.kitchen_path):
            os.mkdir(self.kitchen_path)
        try:
            web_file = urllib2.urlopen(self.build_package_url)
            logging.debug("Build package successfully downloaded: %s" %
                      self.build_package_url)
        except Exception, e:
            raise WorkerError("Cannot download the package to build : %s" %
                        self.build_package_url)
        self.filename = self.build_package_url.split('/')[-1]
        local_tar_file = open(os.path.join(self.kitchen_path, self.filename), 'w')
        local_tar_file.write(web_file.read())
        web_file.close()
        local_tar_file.close()
        local_tar_file = tarfile.open(os.path.join(self.kitchen_path, self.filename), 'r:bz2')
        local_tar_file.extractall(path=os.path.join(self.kitchen_path,
                                                    self.filename.split(".")[0]))
        local_tar_file.close()

    def execute_task(self):
        #a bit of hackery there to import this particular fabfile
        logging.debug("Worker try to execute the task : %s" %
                      self.task)
        file = os.path.join(self.kitchen_path,
                            self.filename.split('.')[0],
                            "fabfile.py")
        file_path = os.path.join(self.kitchen_path, file)
        # We should collect this output
        self.output, self.error = self._execute_task_from_fabfile(file_path,
                                                                  self.task) 
        logging.debug('output : %s' %self.output)
        logging.debug('error : %s' %self.error)
        if self.error:
            self.success = False
            logging.debug("Fail to execute the task")
        else:
            self.success = True
            logging.debug("Succeed to execute the task")
    def post_result(self):
        values = {
            "name": self.name,
            "task": self.task,
            'revision': '',
            'executed':'on',
            'environment':'',
            'output': str(self.output),
            'error':str(self.error),
        }
        if self.success:
            values['success'] = 'on'
        logging.debug("Post the values : %s" %values)
        data = urllib.urlencode(values)
        request = urllib2.Request(self.post_back_url, data)
        fd=urllib2.urlopen(request)
        data=fd.read()
        
    def clean(self):
        logging.debug('Clean the kitchen')
        for f in glob(os.path.join(self.kitchen_path,
                                        self.filename.split('.')[0]+"*")):
            if os.path.isfile(f):
                os.remove(f)
            elif os.path.isdir(f):
                rmtree(f)
    @staticmethod
    def _execute_task_from_fabfile(fabfile_path, task):
        
        fabfile = load_source("fabfile",
                    fabfile_path)
        logging.debug("fabfile_path : %s" %fabfile_path)
        if hasattr(fabfile, task):
            task = getattr(fabfile, task)
            cwd = os.getcwd()
            os.chdir(os.path.dirname(fabfile_path))
            # capture sys.stdout and sys.stderr
            # before executing the task
            output = StringIO()
            error = StringIO()
            sys.stdout = output
            sys.stderr = error
            # execute the task
            try:
                task()
            except SystemExit, e:
                logging.error("%s %s" %(e.__class__(), str(e)))
            finally:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                os.chdir(cwd)
            return (output.getvalue(), error.getvalue())
        else:
            raise WorkerError("No task %s in fabfile %s" %
                                            (task, fabfile_path))    