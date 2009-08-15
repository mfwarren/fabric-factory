import os

WORKER_INTERVAL=600
FABRIC_FACTORY_URL="http://127.0.0.1:8000/factory/build/oldest_not_executed/"
WORKER_PATH = os.path.dirname(os.path.normpath(__file__))
WORKER_KITCHEN = os.path.join(WORKER_PATH, "kitchen")
WORKER_KEEP_BUILDS = True