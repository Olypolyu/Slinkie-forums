from sqlalchemy import create_engine, Column, Integer, String, JSON, ARRAY, LargeBinary, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# move this to a env variable later.
engine = create_engine('postgresql://postgres:1999@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# <tables>
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    passwordHash = Column(String)
    date = Column(Integer)
    permissions = Column(ARRAY(Integer))
    quoteID = Column(Integer)
    follows = Column(ARRAY(Integer))
    blocked = Column(ARRAY(Integer))
    suspendedUntil = Column(Integer)
    settings = Column(JSON)
    

class Content(Base):
    __tablename__ = 'content'
    
    id = Column(Integer, primary_key=True)
    authorID = Column(Integer,  nullable=False)
    contentType = Column(String)
    data = Column(LargeBinary, nullable=True)
    date = Column(Integer)
    deletionDate = Column(Integer, nullable=True)
    
    
class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    
    
class Collection(Base):
    __tablename__ = 'collections'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    authorID = Column(Integer, nullable=False)
    date = Column(Integer)
    body = Column(ARRAY(Integer))


class Thread(Base):
    __tablename__ = 'threads'
    
    id = Column(Integer, primary_key=True)
    categoryID = Column(Integer, nullable=False)
    listAuthorID = Column(ARRAY(Integer))
    display = Column(Integer)
    allowReplies = Column(Boolean)
    allowEdits = Column(Boolean)
    title = Column(String)
    date = Column(Integer)
    deletionDate = Column(Integer)
    body = Column(Integer)
    history = Column(ARRAY(Integer))
    
    
class Reply(Base):
    __tablename__ = 'replies'
    
    id = Column(Integer, primary_key=True)
    authorID = Column(Integer,  nullable=False)
    parentID = Column(Integer)
    threadID = Column(Integer,  nullable=False)
    allowReplies = Column(Boolean)
    allowEdits = Column(Boolean)
    deletionDate = Column(Integer)
    date = Column(Integer)
    body = Column(Integer)
    history = Column(ARRAY(Integer))
    

class Permissions(Base):
    __tablename__ = 'permissions'
    
    roleID = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    color = Column(String)
    canMakeThreads = Column(Boolean)
    canMakeReplies = Column(Boolean)

# </tables>

