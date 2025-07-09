from .user import *
from .chat import *

def init_db():
    Base.metadata.create_all(database.engine)