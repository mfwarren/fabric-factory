import os
import shutil
import subprocess

from fabric.api import local

ve_bin = 'fabric_factory_sandbox/ve/bin'

def bootstrap():
    """
    Create a virtual env called ve and install pip
    """
    local('virtualenv --no-site-packages fabric_factory_sandbox/ve')
    
def install_requirements():
    """
    Install pip and the requirements described in the requirments.txt
    """
    local('%(ve_bin)s/python %(ve_bin)s/easy_install pip'
          %{'ve_bin':ve_bin})
    local('cd fabric_factory_sandbox/fabric_factory; ../../fabric_factory_sandbox/ve/bin/python ../../fabric_factory_sandbox/ve/bin/pip install -r requirements.txt' %{'ve_bin':ve_bin})
    
def install_fabric_factory():
    """
    Add a link from site-package to factory, worker, project 
    """
    local('cd fabric_factory_sandbox/fabric_factory; ../../%(ve_bin)s/python setup.py develop'
          %{'ve_bin':ve_bin})
    

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
    local('%(ve_bin)s/python fabric_factory_sandbox/fabric_factory/src/project/manage.py test --settings=project.settings' %{'ve_bin':ve_bin})

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
    
 
