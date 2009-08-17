from glob import glob
from imp import load_source
from shutil import rmtree
import logging
import os
import simplejson
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
        if not os.path.isdir(self.kitchen_path):
            os.mkdir(self.kitchen_path)
        try:
            web_file = urllib2.urlopen(self.build_package_url)
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
        file = os.path.join(self.kitchen_path,
                            self.filename.split('.')[0],
                            "fabfile.py")
        file_path = os.path.join(self.kitchen_path, file)
        self.output, self.error = self._execute_task_from_fabfile(file_path, self.task)  # We should collect this output
        if self.error:
            self.success = True
        else:
            self.success = False
            
    def post_result(self):
        values = {
            "name":'test',
            "task": 'my_task',
            'revision': '',
            'executed':'on',
            'environment':'',
            'output': str(self.output),
            'error':str(self.error),
        }
        if self.success:
            values['success'] = 'on'
        data = urllib.urlencode(values)
        request = urllib2.Request(self.post_back_url, data)
        fd=urllib2.urlopen(request)
        data=fd.read()
        
    def clean(self):
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
        if hasattr(fabfile, task):
            task = getattr(fabfile, task)
            # execute the task
            output = task()  # We should collect this output
            error = None # TODO : Find a way to collect the error
            return (output, error)
        else:
            raise WorkerError("No task %s in fabfile %s" %
                                            (task, fabfile_path))
    