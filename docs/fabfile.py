import os
import shutil
import subprocess

from fabric.api import local


def bootstrap():
    """
    Create a virtual env called ve and install pip
    """
    local('virtualenv --no-site-packages fabric_factory_sandbox/ve')
    
def install_requirements():
    """
    Install pip and the requirements described in the requirments.txt
    """
    local('. fabric_factory_sandbox/ve/bin/activate; easy_install pip')
    local('. fabric_factory_sandbox/ve/bin/activate; pip install -r fabric_factory_sandbox/fabric_factory/requirements.txt')
    
def install_fabric_factory():
    """
    Add a link from site-package to factory, worker, project 
    """
    local('. fabric_factory_sandbox/ve/bin/activate; python fabric_factory_sandbox/fabric_factory/setup.py develop')
    

def download_fabric_factory():
    """
    Download fabric factory from its repository on bitbucket.org using
    mercurial.
    """
    local('cd fabric_factory_sandbox; hg clone http://bitbucket.org/yml/fabric_factory/')
    
def quickstart():
    """
    All in one command that runs bootstrap, install_requirements,
    project_linkage
    """
    if not os.path.exists("./fabric_factory_sandbox/ve"):
        bootstrap()
    else:
        print "No need to create virtualenv, 've' already exists"
    download_fabric_factory()
    install_requirements()
    install_fabric_factory()
    
def run_test_suite():
    """
    Run the test suite for the Fabric Factory
    """
    local('. fabric_factory_sandbox/ve/bin/activate; python fabric_factory_sandbox/fabric_factory/src/project/manage.py test --settings=project.settings')

def download_setup_and_test():
    """
    This command combine 3 commands :
      * download_fabric_factory
      * quickstart
      * run_test_suite
    """
    print 'starting ...'
    print 'Installing the requirements and fabric_factory'
    quickstart()
    print 'Running the test suite for fabric_factory' 
    run_test_suite()
    print "end"
    
 
