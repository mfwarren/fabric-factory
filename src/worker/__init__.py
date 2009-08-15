import os
import urllib
import urllib2
import simplejson
import tarfile
from glob import glob
from shutil import rmtree

from worker import settings

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
    def download_build_package(self):
        if not os.path.isdir(self.kitchen_path):
            os.mkdir(self.kitchen_path)
        web_file = urllib2.urlopen(self.build_package_url)
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
        from imp import load_source
        file = os.path.join(self.kitchen_path,
                            self.filename.split('.')[0],
                            "fabfile.py")
        fabfile = load_source("fabfile",
                    os.path.join(self.kitchen_path, file))
        if hasattr(fabfile, self.task):
            task = getattr(fabfile,self.task)
            # execute the task
            self.output = task()  # We should collect this output
            self.success = True
            
    def post_result(self):
        values = {
            "name":'test',
            "task": 'my_task',
            'revision': '',
            'executed':'on',
            'environment':'',
            'output': str(self.output)
        }
        if self.success:
            values['success'] = 'on'
        data = urllib.urlencode(values)
        request = urllib2.Request(self.post_back_url, data)
        fd=urllib2.urlopen(request)
        data=fd.read()
        print data   
        
    def clean(self):
        for f in glob(os.path.join(self.kitchen_path,
                                        self.filename.split('.')[0]+"*")):
            if os.path.isfile(f):
                os.remove(f)
            elif os.path.isdir(f):
                rmtree(f)
    