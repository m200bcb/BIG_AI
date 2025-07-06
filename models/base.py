from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

from connect import session

'''DB 생성을 위한 파일'''

Model = declarative_base()
Model.query = session.query_property()


class TimeStampedModel(Model):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    #한국 표준시
    # dt_kst = datetime.utcnow + datetime.timedelta(hours=9)
