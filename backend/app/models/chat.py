from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Dialog(Base):
    __tablename__ = 'dialogs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # Relationship to access messages
    messages = relationship("Message", back_populates="roadmap")

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    is_user = Column(Boolean, nullable=False)
    roadmap_id = Column(Integer, ForeignKey('dialogs.id'), nullable=False)
    
    # Relationship to access the roadmap
    roadmap = relationship("Dialog", back_populates="messages")
