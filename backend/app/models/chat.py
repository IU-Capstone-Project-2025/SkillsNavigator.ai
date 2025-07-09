from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Table, Float
from sqlalchemy.orm import relationship, declarative_base
from app.services import database
import enum

Base = declarative_base()

roadmap_courses = Table(
    'roadmap_courses',
    Base.metadata,
    Column('roadmap_id', Integer, ForeignKey('roadmaps.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    cover_url = Column(String, nullable=True)        # Link to the course cover
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=True)         # Duration in hours
    difficulty = Column(String, nullable=True)         # Easy/Medium/Hard
    price = Column(Integer, nullable=False)            # Course price
    currency_code = Column(String, nullable=True)      # Currency code (e.g., RUB, USD)
    pupils_num = Column(Integer, nullable=False)       # Number of enrolled pupils
    authors = Column(String, nullable=False)            # Can be an empty list, details to be fetched later
    rating = Column(Float, nullable=False)              # Rating from 0 to 5
    url = Column(String, nullable=False)                # Course URL
    description = Column(String, nullable=False)        # Course description
    summary = Column(String, nullable=False)            # Course summary
    target_audience = Column(String, nullable=False)    # Target audience
    acquired_skills = Column(String, nullable=False)    # Skills acquired
    acquired_assets = Column(String, nullable=False)    # Assets acquired
    title_en = Column(String, nullable=False)           # Title in English
    learning_format = Column(String, nullable=False)    # Learning format
    roadmaps = relationship("Roadmap", secondary=roadmap_courses, back_populates="courses")

class RoadmapStatus(enum.Enum):
    current = "current"
    notNow = "notNow"
    done = "done"

class Roadmap(Base):
    __tablename__ = 'roadmaps'
    
    id = Column(Integer, primary_key=True)
    status = Column(Enum(RoadmapStatus), nullable=False)
    name = Column(String, nullable=False)
    courses = relationship("Course", secondary=roadmap_courses, back_populates="roadmaps")

class Dialog(Base):
    __tablename__ = 'dialogs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    owner = Column(Integer, nullable=False)
    roadmap_id = Column(Integer, ForeignKey('roadmaps.id'), nullable=True)
    
    # Relationship to access messages
    messages = relationship("Message", back_populates="dialog")

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    is_user = Column(Boolean, nullable=False)
    dialog_id = Column(Integer, ForeignKey('dialogs.id'), nullable=False)
    
    dialog = relationship("Dialog", back_populates="messages")
    

Base.metadata.create_all(database.engine)