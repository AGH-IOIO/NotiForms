from pymongo import MongoClient


_credentials_filename = "db_credentials"

with open(_credentials_filename) as file:
    _login = file.readline().rstrip()
    _password = file.readline().rstrip()
    _cluster = file.readline().rstrip()

_connection_string = "mongodb+srv://" \
                     + _login + ":" \
                     + _password + "@" \
                     + _cluster \
                     + "-5qtaz.mongodb.net/test?retryWrites=true&w=majority"

db = MongoClient(_connection_string)["noti_forms"]
