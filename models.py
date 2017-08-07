
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    content = Column(String)

    stats = relationship("QuestionStat", back_populates="question")

    def __repr__(self):
        return "<question #%s: %s>" % (self.id, self.content)


class Stat(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)

    stats = relationship("QuestionStat", back_populates="name")

    def __repr__(self):
        return "stat #%s: %s = %s" % (self.id, self.name, self.value)


class QuestionStat(Base):
    __tablename__ = 'question_stats'

    id = Column(Integer, primary_key=True)
    yes = Column(Integer)
    no = Column(Integer)
    question_id = Column(Integer, ForeignKey('questions.id'))
    stat_id = Column(Integer, ForeignKey('stats.id'))

    question = relationship("Question", back_populates="stats")
    name = relationship("Stat", back_populates="stats")

    def __repr__(self):
        # return "<qstat : %s>" % (self.id, self.content)
        return "qstat #%s" % self.id

