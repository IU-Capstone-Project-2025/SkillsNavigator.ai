from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.services import database


class User(database.Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    stepik_id = Column(Integer, unique=True, nullable=False)
    code = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    avatar = Column(String, nullable=True)




