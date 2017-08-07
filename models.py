
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    content = Column(String)

    def __repr__(self):
        return "<question #%s: %s>" % (self.id, self.content)


"""
class QuestionStat(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    yes = Column(Integer)
    no = Column(Integer)

    def __repr__(self):
        return "<question #%s: %s>" % (self.id, self.content)
"""
