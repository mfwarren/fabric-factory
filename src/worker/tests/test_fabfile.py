import os
import shutil

from fabric.api import local


def bootstrap():
    """
    Create a virtual env called ve and install pip
    """
    local('virtualenv fabric_factory/ve')
    
def install_requirements():
    """
    Install pip and the requirements described in the requirments.txt
    """
    local('. fabric_factory/ve/bin/activate; easy_install pip')
    local('. fabric_factory/ve/bin/activate; pip install -r requirements.txt')
    
def project_linkage():
    """
    Add a link from site-package to factory, worker, project 
    """
    current_dir = os.getcwd()
    ve_lib = os.path.join(current_dir, 'fabric_factory', 've', 'lib')
    
    python_version = os.listdir(ve_lib).pop()
    for target_dir in ["project", "worker", "factory"]:
        if not os.path.islink(
            os.path.join(ve_lib, python_version,
                                "site-packages", target_dir)):
            local('ln -s %s %s' %
                  (
                    os.path.join(current_dir,"fabric_factory", "src", target_dir),
                   os.path.join(ve_lib, python_version,
                                "site-packages", target_dir)
                  )
            )
        else:
            print 'link to %s already exists' %target_dir

def download_fabric_factory():
    """
    Download fabric factory from its repository on bitbucket.org using
    mercurial.
    """
    local('hg clone http://bitbucket.org/yml/fabric_factory/')
    
def quickstart():
    """
    All in one command that runs bootstrap, install_requirements,
    project_linkage
    """
    if not os.path.exists("./fabric_factory/ve"):
        bootstrap()
    else:
        print "No need to create virtualenv, 've' already exists"
    install_requirements()
    project_linkage()
    
def run_test_suite():
    """
    Run the test suite for the Fabric Factory
    """
    local('. fabric_factory/ve/bin/activate; fabric_factory/src/project/manage.py test')
    
def download_setup_and_test():
    """
    This command combine 3 commands :
      * download_fabric_factory
      * quickstart
      * run_test_suite
    """
    download_fabric_factory()
    quickstart()
    run_test_suite()
    
 