import os

MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_PORT = os.environ['MYSQL_PORT']
MYSQL_DATABASE = os.environ['MYSQL_DATABASE']

DIMIAPI_URL=os.environ['DIMIAPI_URL']
DIMIAPI_ID=os.environ['DIMIAPI_ID']
DIMIAPI_PW=os.environ['DIMIAPI_PW']

JWT_SECRET=os.environ['JWT_SECRET']
JWT_EXPIRE=int(os.environ['JWT_EXPIRE'])