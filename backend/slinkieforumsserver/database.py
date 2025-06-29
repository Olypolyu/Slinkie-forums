from concurrent.futures import thread
from sqlalchemy import (
    create_engine,
    select, 
    Column,
    Integer,
    String, 
    JSON,
    LargeBinary,
    Boolean, 
    event,
    PrimaryKeyConstraint,
    ForeignKey,
    true
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from hashlib import sha3_256, scrypt
from typing import *
import datetime

unixNow = lambda: datetime.datetime.now().timestamp()

class DISPLAY_ENUM():
    public = 0
    only_authors = 1
    only_link = 2

class ROLE_COLORS_ENUM():
    black = 0
    dark_blue = 1
    dark_green = 2
    dark_aqua = 3
    dark_red = 4
    dark_purple = 5
    gold = 6
    gray = 7
    dark_gray = 8
    blue = 9
    green = 10
    aqua = 11
    red = 12
    light_purple = 13
    yellow = 14
    white = 15
    


# move this to a env variable later.
ENGINE = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=ENGINE)
Base = declarative_base()

# <tables>
class Role(Base):
    __tablename__ = 'roles'
    
    id                  = Column(Integer, primary_key=True)
    name                = Column(String, unique=True, nullable=False)
    color               = Column(Integer, default=15)
    makeThreads         = Column(Boolean)
    makeReplies         = Column(Boolean)
    makeEdits           = Column(Boolean)
    modifyUsers         = Column(Boolean)
    modifyUserPosts     = Column(Boolean)
    editContent         = Column(Boolean)
    deleteContent       = Column(Boolean)
    makeContent         = Column(Boolean)
    hideContent         = Column(Boolean)
    isAdmin             = Column(Boolean)
    suspendUsers        = Column(Boolean)
    banUsers            = Column(Boolean)
    suspendMaxDuration  = Column(Integer, default=datetime.timedelta(days=7).total_seconds())
    
    def __init__(
        self,
        name: str,
        color: ROLE_COLORS_ENUM,

        makeThreads:        bool|None = None,
        makeReplies:        bool|None = None,
        makeEdits:          bool|None = None,
        modifyUsers:        bool|None = None,
        modifyUserPosts:    bool|None = None,
        editContent:        bool|None = None,
        deleteContent:      bool|None = None,
        makeContent:        bool|None = None,
        hideContent:        bool|None = None,
        isAdmin:            bool|None = None,
        suspendUsers:       bool|None = None,
        banUsers:           bool|None = None,
        suspendMaxDuration:       int = int(datetime.timedelta(days=7).total_seconds())
    ):
        self.name = name
        self.color = color
        self.makeThreads = makeThreads
        self.makeReplies = makeReplies
        self.makeEdits = makeEdits
        self.modifyUsers = modifyUsers
        self.modifyUserPosts = modifyUserPosts
        self.editContent = editContent
        self.deleteContent = deleteContent
        self.makeContent = makeContent
        self.hideContent = hideContent
        self.isAdmin = isAdmin
        self.suspendUsers = suspendUsers
        self.banUsers = banUsers
        self.suspendMaxDuration = suspendMaxDuration
        
        
class ROLES_ENUM():
    user = 1
    helper = 2
    admin = 3


@event.listens_for(Role.__table__, 'after_create')
def insert_initial_data(target, connection, **kw):
    session = Session(bind=connection)

    default_roles = [
        Role(
            "User",
            ROLE_COLORS_ENUM.white,
            makeThreads=True,
            makeReplies=True,
            makeEdits=True,
            makeContent=True
        ),
        
        Role(
            "Helper",
            ROLE_COLORS_ENUM.green,
            suspendUsers=True,
            modifyUserPosts=True,
        ),
        
        Role(
            "Admin",
            ROLE_COLORS_ENUM.dark_purple,
            suspendUsers=True,
            suspendMaxDuration=datetime.timedelta(days= 3 * 365).total_seconds(),
            banUsers=True,
            isAdmin=True,
            editContent=True,
            deleteContent=True,
            hideContent=True,
            modifyUsers=True,
            modifyUserPosts=True,
        ),
    ]
    
    session.add_all(default_roles)
    session.commit()
    session.close()



class UserBlock(Base):
    __tablename__ = 'user_blocks'

    blocker_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blocked_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('blocker_id', 'blocked_id'),
    )

class UserFollow(Base):
    __tablename__ = 'user_follows'

    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('follower_id', 'followed_id'),
    )

class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, primary_key=True)
    
class USER_ENUM():
    none = 1

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String) # should this be encrypted? #
    minecraftUUID = Column(String)
    passwordHash = Column(String)
    date = Column(Integer)
    lastLogin = Column(Integer)
    quoteID = Column(Integer)
    suspendedUntil = Column(Integer)
    settings = Column(JSON)


@event.listens_for(User.__table__, 'after_create')
def insert_initial_data(target, connection, **kw):
    session = Session(bind=connection)

    session.add_all([
        User(username = "Herobrine"),
    ])


    session.commit()
    session.close()


class Content(Base):
    __tablename__ = 'content'
    
    id = Column(Integer, primary_key=True)
    authorID = Column(Integer,  nullable=False)
    contentType = Column(String)
    isDataZipped = Column(Boolean)
    isHidden = Column(Boolean, default=False) # will make the content piece hidden from the history. Should be used in case of content that is not ilegal but also unsafe. I **will** remove this all together if i catch someone abusing this.
    data = Column(LargeBinary, nullable=True)
    date = Column(Integer)
    deletionDate = Column(Integer, nullable=True)
    
    def __init__(self, contentType: str, data: bytes, authorID: int = USER_ENUM.none, isZipped: bool = False, date = unixNow()):
        self.contentType = contentType
        self.data = data
        self.isDataZipped = isZipped
        self.date = date
        self.authorID = authorID
        
    def delete(self):
        self.deletionDate = unixNow()
        self.data = b""
        
        
class CONTENT_ENUM():
    deleted = 1
    missing = 2
    none = 3


@event.listens_for(Content.__table__, 'after_create')
def insert_initial_data(target, connection, **kw):
    defaults = [
        Content("text/markdown", b'# [ This piece of Content has been deleted. ]'),
        Content("text/markdown", b'# [ This piece of Content is missing. ]'),
    ]

    session = Session(bind=connection)
    session.add_all(defaults)
    session.commit()
    session.close()
    
    
    
class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    icon = Column(String) # icon is a src for a html img
    description = Column(Integer)
    
    def __init__(self, title:str, description: int = CONTENT_ENUM.missing, icon: str = "/src/assets/talk.png"):
        self.title = title
        self.description = description
        self.icon = icon
        
        
class CATEGORY_ENUM():
    survival = 1
    creative = 2
    redstone = 3
    texture_packs = 4
    fanart = 5
    modding = 6


@event.listens_for(Category.__table__, 'after_create')
def insert_initial_data(target, connection, **kw):
    session = Session(bind=connection)

    category_description = [
        Content("text/markdown", b"General talk about Survival mode"),
        Content("text/markdown", b"General talk about Creative mode"),
        Content("text/markdown", b"Share your Redstone creations!"),
        Content("text/markdown", b"Exercise your pixel art skills!"),
        Content("text/markdown", b"Show-off your art!"),
        Content("text/markdown", b"Fold the very code of BTA to your will."),
    ]
    
    session.add_all(category_description)
    session.commit()
    
    categories = [
        Category("Survival",                   category_description[i:= 0].id),
        Category("Creative",                   category_description[i:= i+1].id),
        Category("Redstone",                   category_description[i:= i+1].id),
        Category("Texture packs",              category_description[i:= i+1].id),
        Category("Fanart",                     category_description[i:= i+1].id),
        Category("Modding - Computer Weirdos", category_description[i:= i+1].id),
    ]

    session.add_all(categories)
    session.commit()
    session.close()
    
    
class Collection(Base):
    __tablename__ = 'collections'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    authorID = Column(Integer, nullable=False)
    date = Column(Integer)

class CollectionContent(Base):
    __tablename__ = 'collection_contents'

    collection_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('collection_id', 'content_id'),
    )

class CONTENT_TYPE_ENUM:
    thread = 0
    reply = 1

class Edit(Base):
    __tablename__ = 'edits'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
    reptacle_id = Column(Integer, nullable=False)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)


class Thread(Base):
    __tablename__ = 'threads'
    
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, nullable=False)
    display = Column(Integer)
    allowReplies = Column(Boolean, default=True, nullable=False)
    allowEdits = Column(Boolean, default=True, nullable=False)
    title = Column(String, nullable=False)
    date = Column(Integer, nullable=False)
    deletionDate = Column(Integer)
    body = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    #history = Column(ARRAY(Integer))
        
    def edit(self, newContent: Content):
        #TODO: move to api
        if self.body is not None:
            if self.history is None: self.history = []
            self.history.append(self.body)
        self.body = newContent.id

class ThreadAuthorship(Base):
    __tablename__ = 'thread_author'

    thread_id = Column(Integer, ForeignKey('threads.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('thread_id', 'user_id'),
    )
    

class Reply(Base):
    __tablename__ = 'replies'
    
    id = Column(Integer, primary_key=True)
    authorID = Column(Integer,  nullable=False)
    parentID = Column(Integer)   # if empty assume parent to be the thread itself.
    threadID = Column(Integer,  nullable=False)
    allowReplies = Column(Boolean)
    allowEdits = Column(Boolean)
    deletionDate = Column(Integer)
    date = Column(Integer)
    body = Column(Integer)
    #history = Column(ARRAY(Integer))
    
    def __init__(self, author: User|int, parent_id: int, thread_id: int, contentID: int = 2, date = unixNow(), **args):
        if self.listAuthorID is None: self.listAuthorID = []
        self.authorID = author.id if isinstance(author, User) else author
        self.body = contentID
        self.date = date
        self.parentID = parent_id
        self.threadID = thread_id
    
        if hasattr(args, 'allowReplies'): self.allowReplies = args['allowReplies']
        else: self.allowReplies = True
        
        if hasattr(args, 'allowEdits'): self.allowEdits = args['allowEdits']
        else: self.allowEdits = True

    def edit(self, newContent: Content|int):
        if type(newContent) == int:
            session = Session()
            newContent = session.query(Content).where(id == newContent).first()
            session.close()
        
        if self.body is not None:
            if self.history is None: self.history = []
            self.history.append(self.body)
        self.body = newContent.id
        
    def delete(self, hideContent: bool = False):
        if hideContent:
            session = Session()
            content = session.query(Content).where(id == self.body).first()
            content.isHidden = True
            session.commit()
            session.close()
        self.edit(CONTENT_ENUM.deleted)

# </tables>

Base.metadata.create_all(ENGINE)