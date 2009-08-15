import urllib2

from django.test.testcases import TestCase
from django.core.urlresolvers import reverse


from factory.tests import create_fabfile_recipe, create_build

from worker.run_worker import worker_factory
from worker import settings


class WorkerTest(TestCase):
    def setUp(self):
        self.fabfile_recipe = create_fabfile_recipe(name="test recipe")
        self.build = create_build(fabfile_recipe=self.fabfile_recipe)
    def test_worker_factory(self):
        options = {
            'factory_url': 'http://127.0.0.1:8000/factory/build/oldest_not_executed/',
            'keep_builds': True, 'interval': 600,
            'kitchen': '/home/yml/workdir/webdev/fabric_factory/ve/lib/python2.6/site-packages/worker/kitchen'}
        
        worker = worker_factory(factory_url=options['factory_url'],
                   kitchen_path=options['kitchen'])
        
