from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from src.db.conn import TABLE_NAME

Base = declarative_base()

class PollInstance(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    latency = Column(Float, nullable=False)
    failed_request = Column(Boolean, nullable=False)
    length_correct = Column(Boolean, nullable=False)
    punctuation = Column(Boolean, nullable=False)

    api_fact = Column(Text, nullable=False)
    api_length = Column(Integer, nullable=False)
