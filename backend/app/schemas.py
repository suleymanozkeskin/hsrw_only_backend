import enum
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint



    

# HASHING THE PASSWORDS FOR SECURITY:  pip install passlib[bcrypt]

############### from zero 


    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr         
    created_at: datetime
                            ## What to return as response 
                            # Without defining the "class Config: ", we will receive an error because pydantic does not know how to work with SqlAlchemy model. 
                            ## This class will tell pydantic to go ahead and conver it to a dictionary
    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # this line will not work if the class UserOut is defined above(before) class Post(Postbase)
    
    class Config:
        orm_mode = True 


class ShowPost(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut


    class Config:
        orm_mode = True






class PostOut(BaseModel):
    
    Post: Post
    
    # likes: int
    # dislikes: int
    
        
    class Config:
        orm_mode = True
    


    
    
class UserCreate(BaseModel): # we are going to inherit from BaseModel
    email: EmailStr ## This is going to make sure its a valid email address // ## pip install email validator !
    password: str  
     


class UserLogin(BaseModel):
    email: EmailStr 
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
    

class TokenData(BaseModel):
    id: Optional[str] = None
    
    
# class Vote(BaseModel):
#     post_id: int
#     dir: conint(ge=-1,le=1) # direction which is going to be an integer "-1" or "1";
    
#     This works perfectly but you can as well create an enum instance to be able to present the exact accepted values:
# from enum import IntEnum
# class Choices(IntEnum):
#     remove  = 0
#     add         = 1
# class Vote(BaseModel):
#     post_id: int
#     direction: Choices
    
    

class EventPost(BaseModel):
    title: str
    content: str
    date: str
    organizer_name: str
    image_url: str
    image_url_type: str


    
    class Config:
        orm_mode = True
    


# class EventPostCreate(BaseModel):
#     event_title: str
#     event_content: str
#     event_date: str
#     organizer_name: str

#     class Config:
#         orm_mode =True

# class EventPostUpdate(BaseModel):
#     event_title: str
#     event_content: str
#     event_date: str
#     organizer_name: str
    
#     class Config: 
#         orm_mode = True
        


class EventPostOut(BaseModel):
    event_title: str
    event_content: str
    event_date: str
    organizer_name: str
    
    class Config:
        orm_mode: True    






    
class TutorPost(BaseModel):
  
    title = str
    content = str
    faculty_name = str
    class_name = str
    
    
    
    class Config:
        orm_mode= True
    
 
class TutorList(BaseModel):
    
    
    class Config:
        orm_mode = True
        
    
    
        
class HireTutor(BaseModel):
    post_title: str
    post_content: str
    employer_email: str
    
    class Config:
        orm_mode = True
        
    
    
    
    
    
    
    
class BeTutor(BaseModel):
    profile_title: str
    profile_explanation: str
    faculty_name: str 
    tutor_gpa: float
    email: str
    hourly_rate: float
    
    
    class Config:
        orm_mode = True



    
class RateTutor(BaseModel):
    RatingScore: conint(ge=0,le=11)
    orm_mode = True    