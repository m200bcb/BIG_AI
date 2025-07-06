from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from models.base import TimeStampedModel, Model

'''DB에서 객체 간 관계 정의'''

class Problem(TimeStampedModel):

    __tablename__ = 'problems'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    pb_no = Column(Integer, nullable=False)
    pb_questions = Column(String(1000), nullable=False)
    pb_answers = Column(String(1000), nullable=True)

    WA = relationship('WA', back_populates='problems', uselist=False)
    dates = relationship('Dates', back_populates='problems')

class WA(TimeStampedModel):

    __tablename__ = 'wa'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(100), nullable=False)
    wrong_answers = Column(String(1000), nullable=False)
    wrong_reasons = Column(String(1000), nullable=False)
    problem_id = Column(
        Integer,
        ForeignKey('problems.id', ondelete='CASCADE'),
        index=True
    )

    problems = relationship('Problem', back_populates='WA')
    dates = relationship('Dates', back_populates='wrong_answers')

class Dates(TimeStampedModel):

    __tablename__ = 'dates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dates = Column(String(80), nullable=False)
    wa_id = Column(Integer, ForeignKey('wa.id', ondelete='CASCADE'), nullable=False)
    pb_id = Column(Integer, ForeignKey('problems.id', ondelete='CASCADE'), nullable=False)

    wrong_answers = relationship('WA', back_populates='dates')
    wrong_reasons = relationship('WA', back_populates='dates')
    problems = relationship('Problem', back_populates='dates')
