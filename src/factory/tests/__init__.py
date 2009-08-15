"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import os
from django.conf import settings
from django.test import TestCase
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from factory.models import FabfileRecipe, Build
from factory.views import build_lists

def create_fabfile_recipe(name):
    TEST_FABFILE = os.path.join(
        os.path.dirname(os.path.normpath(__file__)),
        'test_fabfile.py')
    with open(TEST_FABFILE) as f:
        fabfile_recipe = FabfileRecipe()
        fabfile_recipe.name = name
        fabfile_recipe.slug = slugify(name)
        fabfile_recipe.file.save(os.path.basename(f.name),
                                 ContentFile(f.read()))
        fabfile_recipe.save()
        return fabfile_recipe
    
def create_build(fabfile_recipe):
    build =  Build()
    build.name = "test build"
    build.task = "hello_world"
    build.fabfile_recipe = fabfile_recipe
    build.save()
    return build

class FabfileRecipeApiTest(TestCase):
    def test_create_fabfile_recipe(self):
        """
        Create a FabfileRecipe and attach a fabfile
        """
        self.assertEqual(FabfileRecipe.objects.count(), 0)
        fabfile_recipe = create_fabfile_recipe(name="test recipe")
        self.assertEqual(FabfileRecipe.objects.count(), 1)
        
class CreateBuildApiTest(TestCase):
    def setUp(self):
        self.fabfile_recipe = create_fabfile_recipe(name="test recipe")
    def test_create_build(self):
        self.assertEqual(Build.objects.count(), 0)
        build = create_build(fabfile_recipe=self.fabfile_recipe)
        self.assertEqual(Build.objects.count(), 1)
        
class BuildApiTest(TestCase):
    def setUp(self):
        self.fabfile_recipe = create_fabfile_recipe(name="test recipe")
        self.build = create_build(fabfile_recipe=self.fabfile_recipe)
    def test_make_build_package(self):
        filename = self.build.make_build_package()
        self.assertEqual(
            os.path.isfile(os.path.join(settings.BUILD_PATH, filename)),
            True)
    def test_get_build_package_url(self):
        url = self.build.get_build_package_url()
        
class BuildDetailUrlTest(TestCase):
    def setUp(self):
        self.fabfile_recipe = create_fabfile_recipe(name="test recipe")
        self.build = create_build(fabfile_recipe=self.fabfile_recipe)
    def test_build_detail_get(self):
        response = self.client.get(reverse("factory.views.build_detail",
                                           kwargs={'object_id':self.build.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'],
                         self.build)
                                   
                                   
class BuildlistUrlTest(TestCase):
    def setUp(self):
        self.fabfile_recipe = create_fabfile_recipe(name="test recipe")
        self.build = create_build(fabfile_recipe=self.fabfile_recipe)
    def test_build_list_get(self):
        response = self.client.get(reverse(build_lists['all']))
        self.assertEqual(list(response.context['object_list']),
                         list(Build.objects.all()))
    def test_build_list_success_get(self):
        response = self.client.get(reverse(build_lists['success']))
        self.assertEqual(list(response.context['object_list']),
                         list(Build.objects.filter(success=True)))
    def test_build_list_no_success_get(self):
        response = self.client.get(reverse(build_lists['no_success']))
        self.assertEqual(list(response.context['object_list']),
                         list(Build.objects.filter(success=False)))
    def test_build_list_executed_get(self):
        response = self.client.get(reverse(build_lists['executed']))
        self.assertEqual(list(response.context['object_list']),
                         list(Build.objects.filter(executed=True)))
    def test_build_list_not_executed_get(self):
        response = self.client.get(reverse(build_lists['not_executed']))
        self.assertEqual(list(response.context['object_list']),
                         list(Build.objects.filter(executed=False)))
        
class BuildUpdateUrlTest(TestCase):
    def setUp(self):
        self.fabfile_recipe = create_fabfile_recipe(name="test recipe")
    def test_build_create_get(self):
        response = self.client.get(reverse("factory.views.build_create",
                                           kwargs={}))
        self.assertEqual(response.status_code, 200)
    def test_build_update_post(self):
        self.assertEqual(Build.objects.count(), 0)
        response = self.client.post(reverse("factory.views.build_create",
                                           kwargs={}),
                                   {"name":'test',
                                    "task": 'my_task',
                                    "fabfile_recipe":str(self.fabfile_recipe.id),
                                    'revision': '',
                                    'executed':'',
                                    'success':'',
                                    'environment':'',
                                    'output':''
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Build.objects.count(), 1)
        
class BuildOldestNotExecutedUrlTest(TestCase):
    def setUp(self):
        self.fabfile_recipe = create_fabfile_recipe(name="test recipe")
        self.build = create_build(fabfile_recipe=self.fabfile_recipe)
        
    def test_build_oldest_not_executed_get(self):
        response = self.client.get(reverse("factory.views.build_oldest_not_executed",
                                           kwargs={}))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 
        '{"task": "hello_world", "name": "test build", "build_package_url":')
        self.assertContains(response, 
        '"post_back_url": "http://example.com/factory/build/update/1/"}')
        
    def test_build_oldest_not_executed_empty_get(self):
        self.build.executed = True
        self.build.save()
        response = self.client.get(reverse("factory.views.build_oldest_not_executed",
                                           kwargs={}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'false')
        
        
        
