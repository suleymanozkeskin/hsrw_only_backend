# new models.py
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Float, REAL,DateTime,Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import enum
from .database import Base

class User(Base):  ## every class is gonna extend base , its a requirement of SQLALCHEMY model.
    __tablename__= "users"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    



class Forum_Post(Base):
    __tablename__ = "forum_posts"
    id = Column(Integer, primary_key=True,nullable=False,autoincrement=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default="TRUE",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id"), nullable=False)    
    dislikes = Column(Integer,server_default="0",relationship="User")
    likes = Column(Integer,server_default="0")
    

class Event_Post(Base):
    __tablename__ = "event_posts"
    id = Column(Integer, primary_key=True,nullable=False,autoincrement=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default="TRUE",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    
    #many to many relationship
    attendees = relationship("User",secondary="event_attendees")
    
