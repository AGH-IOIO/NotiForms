import os
from pymongo import MongoClient


_db_conn_string = "mongodb://%s:%s@%s:%s" % (
    os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"],
    os.environ["DB_HOSTNAME"], os.environ["DB_PORT"]
)
conn = MongoClient(_db_conn_string)
db = conn[os.environ["DB_NAME"]]
