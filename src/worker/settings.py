import os
import logging

DEBUG = True

WORKER_INTERVAL = 3 # Interval in second
FABRIC_FACTORY_URL = "http://127.0.0.1:8000/factory/build/oldest_not_executed/"
WORKER_PATH = os.path.dirname(os.path.normpath(__file__))
WORKER_KITCHEN = os.path.join(WORKER_PATH, "kitchen")
WORKER_KEEP_BUILDS = True


##################################################
# logging
#
# Set the logging level to control the volume of emitted log messages.
# Use logging.DEBUG to emit all log messages. To get progressively fewer
# messages use logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
#
LOGGING_LEVEL = (logging.DEBUG if DEBUG else logging.WARNING)
# Use this to change the filename and/or location of the logfile as needed.

LOGGING_LOGFILE = 'worker.log'
# You probably won't need to change the following default settings

LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOGGING_DATEFMT = "%m-%d %H:%M:%S"
 
# Uncomment this call to basicConfig code to enable logging.
# (Some deployments will require advanced logging configuration.
# In that case, substitute that logging setup code here instead.)

logging.basicConfig(level=LOGGING_LEVEL,
                    format=LOGGING_FORMAT,
                    datefmt=LOGGING_DATEFMT,
                    filename=LOGGING_LOGFILE,
                    filemode="a")

try:
    from project import local_settings
except:
    pass

