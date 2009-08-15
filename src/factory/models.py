import tarfile
import bz2
import tempfile
import os
from cStringIO import StringIO


from django.db import models
from django.conf import settings

# Create your models here.

class FabfileRecipe(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    file = models.FileField(upload_to='factory/fabfiles')

    
class Build(models.Model):
    name = models.CharField(max_length=255)
    task = models.CharField(max_length=255,
                            help_text='Space separated list of tasks')
    fabfile_recipe = models.ForeignKey(FabfileRecipe)
    revision = models.CharField(max_length=255, null=True, blank=True)
    executed = models.BooleanField()
    success = models.BooleanField()
    environement = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    def make_build_package(self):
        """
        This method should build a compressed package containing the task runner,
        the fabfile. The task runner will be a python script that will execute
        the targeted tasks from the fabfile.
        """
        
        # Check if BUILD_PATH exist if it doesn't create it
        if not os.path.isdir(settings.BUILD_PATH):
            os.mkdir(settings.BUILD_PATH)
        # Make a tar of all the required files
        dst = tempfile.mktemp(prefix="%s_%s" %(self.id ,self.fabfile_recipe.slug),
                              suffix=".tar.bz2",
                              dir=settings.BUILD_PATH)
        try:
            out_tarfile = tarfile.TarFile.open(dst, mode="w:bz2")
            file = os.path.abspath(self.fabfile_recipe.file.path)
            
            out_tarfile.add( file, arcname='fabfile.py' )
            build_runner = "fab %s" %self.task
            info = tarfile.TarInfo(name='build_runner.py')
            info.size = len(build_runner)
            out_tarfile.addfile(info, StringIO(build_runner))
            tarfile_name  = out_tarfile.name
            return os.path.basename(tarfile_name)
        finally:
            out_tarfile.close()
            
            
    def get_build_package_url(self):
        filename = self.make_build_package()
        return "%s/%s" %(settings.BUILD_URL, filename)

