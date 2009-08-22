from fabric.api import local

def hello_world():
    """
    Say hello to the world
    """
    print "hello world"
    local('ls -l')
