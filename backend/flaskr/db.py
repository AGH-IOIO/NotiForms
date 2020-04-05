import os
from pymongo import MongoClient


_db_conn_string = "mongodb://%s:%s@%s:%s" % (
    os.environ['DB_USERNAME'], os.environ['DB_PASSWORD'],
    os.environ['DB_HOSTNAME'], os.environ['DB_PORT']
)
db = MongoClient(_db_conn_string)[os.environ['DB_NAME']]
