from turtle import title
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    tags=["Event_Posts"]
)



@router.get("/event_posts", response_model=List[schemas.EventPost]) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
   
    
    print(search)

    
    posts = db.query(models.Event_Post).all()
    return posts  
    
    
   
    
    



@router.post("/event_posts",status_code=status.HTTP_201_CREATED, response_model=schemas.EventPost)
def create_posts(post: schemas.EventPost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     
    
    new_post = models.Event_Post(organizer_id = current_user.id,  **post.dict()) ## this method will take the post as dictionary and automatically import it from there as opposed to manual typing version below:
    # new_post = models.Post(title=post.title, content=post.content , published= post.published)
    
    #new_post = models.Event_Post(organizer_id=current_user.id, event_title=models.Event_Post.event_title , event_content=models.Event_Post.event_content, organizer_name=models.Event_Post.organizer_name, event_date=models.Event_Post.event_date)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve new post 
    return new_post






@router.get("/event_posts/{id}", response_model=schemas.EventPost) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    post = db.query(models.Event_Post).filter(models.Event_Post.id == id).first()
    #post = post.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.")
        
    if post.organizer_id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    return post


    
#     # IMPORTANT NOTE !!
#     # Issue: In order to avoid receiving id numbers in a non-integer form like this: http://127.0.0.1:8000/posts/asdjsdsfds , 
#     # We need to first validate it as a number and convert into an integer as we define in the get_post function.
#     # Then we have to convert back in to a string when we want execute our SQL Query, OTHERWISE there will be a " TypeError: 'int' object does not support indexing. "
    

    







@router.delete("/event_posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # deleting posts
    # find the index in the array that has the required ID
    # my_posts.pop(index)
    
    #cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING* """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    
    post_query = db.query(models.Event_Post).filter(models.Event_Post.id == id )   # we define the post here

    post = post_query.first() # then we find that post by using .first()
    
    if post == None:  # then we will check if the post is not there 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
    if post.organizer_id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED,detail="Not authorized to perform requested action." )
    
    
    post_query.delete(synchronize_session=False)  # and finally if everything checks out , we will let them to delete the post.
    db.commit()
      
    # IMPORTANT NOTE ON     @app.delete and HTTP_204_NO_CONTENT : 
    # if we delete something , we can not return a data like this: 
    # return{"post_detail": post}
    # instead we have to use FAST-API's Response feature 
    # and return whatever the status code is.
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 



@router.put("/event_posts/{id}",response_model=schemas.EventPost)
def update_post(id: int , updated_post: schemas.EventPost, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
   
    post_query = db.query(models.Event_Post).filter(models.Event_Post.id == id)
    
    post = post_query.first()
            
    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
    if post.organizer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail="Not authorized to perform requested action." )
    
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
        
    #''' post_dict = post.dict() # convert the data we get from "post: Post" to a dictionary 
    #post_dict["id"] = id  # we are gonna ad id to dictionary 
    #my_posts[index] = post_dict # and for that spesific id, index  we will replace with the new dictionary '''

   
    return post_query.first()





