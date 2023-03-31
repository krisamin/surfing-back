from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app import setting

db_url: str = 'mysql+pymysql://{username}:{password}@{db_host}:{db_port}/{db_name}'.format(
    username=setting.MYSQL_USER,
    password=setting.MYSQL_PASSWORD,
    db_host="surfing-mariadb",
    db_port=setting.MYSQL_PORT,
    db_name=setting.MYSQL_DATABASE
)

try:
    engine = create_engine(db_url, pool_recycle=3600)
    db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except:
    raise NotImplementedError

def get_db():
    db: Session = db_session()
    try:
        yield db
    finally:
        db.close()
