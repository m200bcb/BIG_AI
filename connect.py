'''
DB 생성
python
from connect import engine
from models.base import Model
from models.tables import *
Model.metadata.create_all(engine)
'''

import os

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import scoped_session, sessionmaker

'''DB 생성을 위한 파일'''

# 데이터베이스 파일 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = 'users.db'

engine = create_engine(f"sqlite:///{BASE_DIR}/{DB_NAME}", echo=True) #echo는 로그를 위한 플래그

session = scoped_session(
    sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=engine
    )
)

@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()
