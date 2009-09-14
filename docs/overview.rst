Fabric factory
==============

This is a project I have been working on recently after I spent a day to look at the existing solution to run periodically a test suite. Most of the project I look at were either difficult to setup or require to learn yet another specific domain specific language or had dependency on a larger software stack.

As a reaction to this situation I have decided to see if I could write something simple that achieve gracefully the task above. I also try to make it as easy to setup as possible.  

In order to achieve this I have decided to use cpython as platform, django as web framework for the server and Fabric as library to automate the task execution.

The result of this mix can be found on bitbucket in a project called Fabric Factory (http://bitbucket.org/yml/fabric_factory/). This will eventually become a complete Job Server that could be used to distribute any kind of task scripted in Fabric.


Installation
=============

This assumes that python is installed on your computer and that you have an internet conection.

You can download the code using mercurial:
   * hg clone http://bitbucket.org/yml/fabric_factory/
 A fabfile will help you to quickly setup your environment.
   * fab quickstart
 
 Note : In order to run the command above you will need the latest version of Fabric the following command will take care of this:

  * pip install -e git://github.com/bitprophet/fabric.git#egg=Fabric
  
  Usage
  ======
  
"quickstart" has created a virtual env which must be actived before you run any of the following command.
  * . ve/bin/activate
    
Once the virtualenv is activated you can go inside "src/project". This is a django project so from there you can do several things :

  * create an sqlite db :  python manage.py syncdb
  * run the server : python manage.py runserver
  * run the test suite : python manage.py test

The main app of this django project called fabric factory is called "factory". 

Once the server is started and that you have created some "Build" in django's admin interface you can open a new terminal and run the client side of the project:

  * cd src/worker
  * python run_worker.py --daemon=start
  * python run_worker.py --daemon=stop
  
  Use case
  =========
  
  Now that you have understood the layout of the project. Let us see how achieve something useful with it.
  
We are going to create a Build that will :
    * download the Fabric Factory 
    * setup the environement
    * run the test suite
    * Report the result
    
 1> Direct your browser to that url http://127.0.0.1:8000/admin/ and key in the username/password you have chosen for your administrator.
 2> Add the fabfile recipe store in docs http://127.0.0.1:8000/admin/factory/fabfilerecipe/add/ and call it "fabric factory use case"
 3> Create a Build that will download setup and run the test here : http://127.0.0.1:8000/admin/factory/build/add/
 
The fabfile recipe that we have download earlier contains a task called : 'download_setup_and_test' This task as been writen to do what we want.
 
We are now going to configure the client to run this task. However before doing this let us see how the server publish the tasks that need to be executed. Point your browser to this url : http://127.0.0.1:8000/factory/build/oldest_not_executed/ You can see here a json string describing the task.
 
 """
 {"task": "download_setup_and_test", "name": "download setup and run the test", "build_package_url": "http://127.0.0.1:8000/site_media/build_packages/1_fabric-factory-use-case4fIWt6.tar.bz2", "post_back_url": "http://127.0.0.1:8000/factory/build/update/1/"}
 """
 

Conclusion
===========

This project which is still very immature seems to prove that this stack is well suited to build this kind of tool. I would be glad to hear your experience about this kind of tool. Please do not hesitate to copy, fork, contribute to this project to make sure that soon we have a simple easy to setup yet flexible tool to distribute tasks.
