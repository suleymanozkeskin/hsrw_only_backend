from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Float, REAL,DateTime,Enum
from sqlalchemy.orm import relationship,backref
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import enum
from .database import Base

## IMPORTANT NOTE: SQLAlchemy does not allow us to modify an existing table.We have to drop it and create it again.However there are database migration tools such as ALEMBIC.
#  Which allows us to work around this limitation.
# !pip install alembic

# alembic --help

# alembic init alembic  --> This creates a directory for alembic and alembic.ini out of directory.

# alembic revision --help  



# from .database import Base


## CREATING A TABLE THROUGH ORM:

class User(Base):  ## every class is gonna extend base , its a requirement of SQLALCHEMY model.
    __tablename__= "users"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    #username = Column(String,nullable=False,unique=True)
    
    def __repr__(self):
        return f"User({self.email})"


class Post(Base): # FORUM POST
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,nullable=False,autoincrement=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default="TRUE",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id"), nullable=False)    
    user = relationship("User", backref=backref("user_posts", uselist=True, cascade="delete,all"))
    likes = relationship("Like", backref=backref("likes_posts", uselist=True, cascade="delete,all"))
    dislikes = relationship("Dislike", backref=backref("dislikes_posts", uselist=True, cascade="delete,all"))
    
    
    # The code below will create automatically another property for our post , so when we retrieve a post its going to return it and figure out a relationship between post and user.
    owner = relationship("User") ## Here we are not referencing the table , we are referencing the actual SQLALCHEMY class as below:  class User(Base):


class Like(Base):
    __tablename__= "likes"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("user_likes", uselist=True, cascade="delete,all"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", backref=backref("post_likes", uselist=True, cascade="delete,all"))

    def __repr__(self):
        return f"Like(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at}, user_id={self.user_id}, post_id={self.post_id})"

class Dislike(Base):
    __tablename__= "dislikes"
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("user_dislikes", uselist=True, cascade="delete,all"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", backref=backref("post_dislikes", uselist=True, cascade="delete,all"))

    def __repr__(self):
        return f"Dislike(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at}, user_id={self.user_id}, post_id={self.post_id})"
   
    
    


    
class Event_Post(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True,nullable=False,autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date = Column(String, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))
    organizer_name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    image_url_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    
class Tutor_List(Base):
    __tablename__ = "tutor_lists"
    id = Column(Integer,primary_key=True, nullable=False,autoincrement=True)
    email = Column(String, ForeignKey("users.email",ondelete="CASCADE"),primary_key=True)
    grade = Column(Float, nullable=False) 
    class_name = Column(String, nullable=False)
    
    
class Be_Tutor(Base):
    __tablename__ = "be_tutor_posts"
    id = Column(Integer, primary_key=True,nullable=False,unique=True,autoincrement=True)
    profile_title = Column(String, nullable=False)
    profile_explanation = Column(String, nullable=False)
    faculty_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    tutor_gpa = Column(Float, nullable=False)
    hourly_rate =Column(Float)
    
    email = Column(String, ForeignKey("users.email",ondelete="CASCADE"),primary_key=True)
    
    
class Hire_Tutor(Base):
    __tablename__ = "hiring_tutors_posts"
    id = Column(Integer, primary_key=True,nullable=False,autoincrement=True)
    post_title = Column(String, nullable=False)
    post_content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    employer_email = Column(String, ForeignKey("users.email",ondelete="CASCADE"),primary_key=True)
    
 
 
