import os
import shutil
import subprocess

from fabric.api import local


def bootstrap():
    """
    Create a virtual env called ve and install pip
    """
    local('virtualenv --no-site-packages ve')
    
def install_requirements():
    """
    Install pip and the requirements described in the requirments.txt
    """
    local('. ve/bin/activate; easy_install pip')
    local('. ve/bin/activate; pip install -r requirements.txt')
    
def install_fabric_factory():
    """
    install fabric_factory using setup.py develop. 
    """
    local('. ve/bin/activate; python setup.py develop')


def quickstart():
    """
    All in one command that runs bootstrap, install_requirements,
    project_linkage
    """
    if not os.path.exists("./ve"):
        bootstrap()
    else:
        print "No need to create virtualenv, 've' already exists"
    install_requirements()
    install_fabric_factory()
    
def run_test_suite():
    """
    Run the test suite for the Fabric Factory
    """
    print local('. ve/bin/activate; src/project/manage.py test --settings=project.settings')
    
def temp_clean_up():
    """
    Clean up the environment this command should be used carefully because it
    deletes a lot of stuff:
        * src/project/media/build_packages
        * src/worker/kitchen
    """
    current_dir = os.getcwd()
    file_for_deletion = (
        os.path.join(current_dir,"src" , "project", "media", "build_packages"),
        os.path.join(current_dir,"src" , "worker", "kitchen"),
    )
    for f in file_for_deletion:
        try:
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)
        except Exception, e:
            print e
    
def clean_up():
    """
    Clean up the environment this command should be used carefully because it
    deletes a lot of stuff:
        * src/project/dev.db
        * src/project/media/factory/fabfiles
        * src/project/media/build_packages
        * src/worker/kitchen
    """
    current_dir = os.getcwd()
    file_for_deletion = (
        os.path.join(current_dir,"src" , "project", "dev.db"),
        os.path.join(current_dir,"src" , "project", "media", "factory", "fabfiles"),
        os.path.join(current_dir,"src" , "project", "media", "build_packages"),
        os.path.join(current_dir,"src" , "worker", "kitchen"),
    )
    for f in file_for_deletion:
        try:
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)
        except Exception, e:
            print e
    
