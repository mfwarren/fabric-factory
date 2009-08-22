import os
import urllib2

from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

from factory.tests import create_fabfile_recipe, create_build
from worker import WorkerError
from worker import Worker
from worker import settings

def create_worker():
    kitchen_path = settings.WORKER_KITCHEN
    worker_dict = {u'task': u'hello_world',
                   u'name': u'my build',
                   u'build_package_url': u'http://example.com/site_media/build_packages/1_recipeotPIHY.tar.bz2',
                   u'post_back_url': u'http://example.com/factory/build/update/1/'}
    worker = Worker(name=worker_dict['name'], task=worker_dict['task'],
                post_back_url=worker_dict['post_back_url'],
                build_package_url=worker_dict['build_package_url'],
                kitchen_path=kitchen_path)
    return worker

class WorkerTest(TestCase):
    def setUp(self):
        self.fabfile_recipe = create_fabfile_recipe(name="test recipe")
        self.build = create_build(fabfile_recipe=self.fabfile_recipe)
    def test_create_worker(self):
        """
        Test that I can build a Worker
        """
        worker = create_worker()
        
        
    def test_worker_download_build_package_wrong_url(self):
        worker = create_worker()
        try:
            worker.download_build_package()
        except Exception, e:
            self.assertEqual(True, isinstance(e, WorkerError))
    
class ExecuteTaskFromFabfile(TestCase):
    def setUp(self):
        self.fabfile_path = os.path.join(
            os.path.dirname(os.path.normpath(__file__)),
            "test_fabfile.py"
        )
        self.task = "hello_world"
        self.wrong_task = "wrong task"
        
    def test_execute_task_from_fabfile(self):
        output, error = Worker._execute_task_from_fabfile(self.fabfile_path, self.task)
        self.assertEqual(output, 'hello world\n[localhost] run: ls -l\n')
        self.assertEqual(error, "")
        
    def test_execute_wrong_task_from_fabfile(self):
        try:
            output, error = Worker._execute_task_from_fabfile(self.fabfile_path, self.wrong_task)
        except Exception, e:
            self.assertEqual(True, isinstance(e, WorkerError))
            
#class FaillingTest(TestCase):
#    def test_faillure(self):
#        self.assertEqual(True, False)
