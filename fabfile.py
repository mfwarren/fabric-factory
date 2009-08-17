import os
import shutil

from fabric.api import local


def bootstrap():
    """
    Create a virtual env called ve and install pip
    """
    local('virtualenv ve')
    local('. ve/bin/activate; easy_install pip')
    
def install_requirements():
    """
    Install the requirements described in the requirments.txt
    """
    local('. ve/bin/activate; pip install -r requirements.txt')
    
def project_linkage():
    """
    Add a link from site-package to factory, worker, project 
    """
    current_dir = os.getcwd()
    python_version = "python2.6"
    for target_dir in ["project", "worker", "factory"]:
        local('ln -s %s %s' %
              (
                os.path.join(current_dir,"src", target_dir),
               os.path.join(current_dir, "ve", "lib", python_version,
                            "site-packages", target_dir)
              )
        )


def quickstart():
    """
    All in one command that runs bootstrap, install_requirements,
    project_linkage
    """
    bootstrap()
    install_requirements()
    project_linkage()
    
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
    