from turtle import title
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2,database
from ..database import get_db


from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors





router = APIRouter(
    tags=["Tutor_Profile"]
)



@router.get("/tutor_list", response_model=List[schemas.BeTutor]) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_tutor_profiles(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
   
    
    print(search)

    
    posts = db.query(models.Be_Tutor).all()
    return posts  
    
    
   
    
    




@router.post("/tutor_profile",status_code=status.HTTP_201_CREATED, response_model=schemas.BeTutor)
def create_tutor_profile(post: schemas.BeTutor, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     
    
    #lets check if the logged in user is matching with the user who is trying to create the post:
    if post.email != current_user.email: # then we will check if the user who is logged in , actually owns the post
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )


    #lets check if the user has already created a profile:
    profile = db.query(models.Be_Tutor).filter(models.Be_Tutor.id == current_user.id).first()
    if profile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You already have a profile." )


    else:
        try:
            new_post = models.Be_Tutor(id = current_user.id,  **post.dict()) 
        
            db.add(new_post)
            db.commit()
            db.refresh(new_post) # retrieve new post 
            return new_post

        except UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tutor profile with this credentials already exist")




  






@router.get("/tutor_profile/{id}", response_model=schemas.BeTutor) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_tutor_profile(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
 
    post = db.query(models.Be_Tutor).filter(models.Be_Tutor.id == id).first()
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tutor profile with id: {id} was not found.")
        
    if post.id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    return post


    

    

    







@router.delete("/tutor_profile/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_tutor_posts(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
 
    
    
    post_query = db.query(models.Be_Tutor).filter(models.Be_Tutor.id == id )   # we define the post here

    post = post_query.first() # then we find that post by using .first()
    
    if post == None:  # then we will check if the post is not there 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Tutor profile with id: {id} does not exist.")
        
    if post.id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    
    post_query.delete(synchronize_session=False)  # and finally if everything checks out , we will let them to delete the post.
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 







@router.put("/tutor_profile/{id}",response_model=schemas.BeTutor)
def update_tutor_profiles(id: int ,  updated_post: schemas.BeTutor, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    
    #lets check if mail that user wants to update is already in our database or not:
    email_query = db.query(models.Be_Tutor).filter(models.Be_Tutor.email == updated_post.email).first()

    if not email_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This mail does not exist in our database.")
   
    post_query = db.query(models.Be_Tutor).filter(models.Be_Tutor.id == id)
    
    post = post_query.first()
            
    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Tutor profile with id: {id} does not exist.")
     
    # if post.tutor_email == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail = f"following tutor email: {tutor_email} does not exist.",tutor_email)


    if post.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail="Not authorized to perform requested action." )
    

        
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
        
    #''' post_dict = post.dict() # convert the data we get from "post: Post" to a dictionary 
    #post_dict["id"] = id  # we are gonna ad id to dictionary 
    #my_posts[index] = post_dict # and for that spesific id, index  we will replace with the new dictionary '''

   
    return post_query.first()


##"post_faculty_name" : "Technology and Bionics",
    #"class_name" : "Programming"
    









# lets get a list of employers who are looking for tutors:

@router.get("/employer_list", response_model=List[schemas.HireTutor])
def get_employer_list(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        
        posts = db.query(models.Hire_Tutor).all()
        
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"There is no employer who is looking for a tutor.")
            

        return posts






