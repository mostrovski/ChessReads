import json

DB_NAME = 'database name goes here'
DB_USER = 'database user name goes here'
DB_PASSWORD = 'database user password goes here'
DB_CONNECT = 'postgresql://'+DB_USER+':'+DB_PASSWORD+'@localhost/'+DB_NAME

APP_KEY = 'application key goes here'
APP_NAME = 'Chess Reads'
CLIENT_ID = json.loads(open(
    'client_secrets.json', 'r').read())['web']['client_id']
