from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    tags=["Posts"]
)


# get all posts
@router.get("/posts", response_model=List[schemas.ShowPost])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts





    
    



@router.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """ , (post.title, post.content, post.published)) ##  placeholders , this way we avoid SQL INJECTION! 
    # new_post = cursor.fetchone()
    # conn.commit() ## this is going to push those changes that we do in the postman to the actual database 
    
    
    
    new_post = models.Post(owner_id=current_user.id,  **post.dict()) ## this method will take the post as dictionary and automatically import it from there as opposed to manual typing version below:
    # new_post = models.Post(title=post.title, content=post.content , published= post.published)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve new post 
    return new_post





### ''' @app.post("/posts",status_code=status.HTTP_201_CREATED)
###         def create_posts(post: Post):
###             post_dict = post.dict()
###             post_dict["id"] = randrange(0,100000)
###             my_posts.append(post_dict)
###             return{"data": post_dict} '''




''' @router.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}
     '''
@router.get("/posts/{id}", response_model=schemas.Post) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #post = post.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.")
        
    if post.owner_id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    return post

# @router.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id: int, db: Session = Depends(get_db)):
    
#     # IMPORTANT NOTE !!
#     # Issue: In order to avoid receiving id numbers in a non-integer form like this: http://127.0.0.1:8000/posts/asdjsdsfds , 
#     # We need to first validate it as a number and convert into an integer as we define in the get_post function.
#     # Then we have to convert back in to a string when we want execute our SQL Query, OTHERWISE there will be a " TypeError: 'int' object does not support indexing. "
    
#    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)) ) 
#    # post = cursor.fetchone()
#    # print(post)
    

    
#     if not post: # if we didnt find the post, we will raise an exception using Fast-Api's HTTPException method.
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail= f"post with id: {id} was not found. ")
    
#     return{post}





@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # deleting posts
    # find the index in the array that has the required ID
    # my_posts.pop(index)
    
    #cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING* """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    
    post_query = db.query(models.Post).filter(models.Post.id == id )   # we define the post here

    post = post_query.first() # then we find that post by using .first()
    
    if post == None:  # then we will check if the post is not there 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
    if post.owner_id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    
    post_query.delete(synchronize_session=False)  # and finally if everything checks out , we will let them to delete the post.
    db.commit()
      
    # IMPORTANT NOTE ON     @app.delete and HTTP_204_NO_CONTENT : 
    # if we delete something , we can not return a data like this: 
    # return{"post_detail": post}
    # instead we have to use FAST-API's Response feature 
    # and return whatever the status code is.
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 



@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int , updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    #cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s  RETURNING* """ , (post.title, post.content,post.published,(str(id))) )
    #post_updated = cursor.fetchone() 
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
            
    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail="Not authorized to perform requested action." )
    
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
        
    #''' post_dict = post.dict() # convert the data we get from "post: Post" to a dictionary 
    #post_dict["id"] = id  # we are gonna ad id to dictionary 
    #my_posts[index] = post_dict # and for that spesific id, index  we will replace with the new dictionary '''

   
    return post_query.first()



# testing sqlalchemy Db session with depends
@router.get("/sqlalchemy_test_post")
def test_post(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    
    return posts 







# like a post:
@router.post("/posts/{id}/like")
def like_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        
        post = db.query(models.Post).filter(models.Post.id == id).first()
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} was not found.")
            
        # if post.owner_id == current_user.id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

# we will check if the user has already liked the post or not:
        if db.query(models.Like).filter(models.Like.post_id == id, models.Like.user_id == current_user.id).first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

        like = models.Like(user_id = current_user.id, post_id = id)
        db.add(like)
        db.commit()
        db.refresh(like)

        return like






##### !!!!!!!!!!!!!!!!!!!!!!  
# unlike a post:  ### THIS SECTION IS NOT WORKING PROPERLY , IT CAUSES TO DELETE THE POST INSTEAD OF DELETING THE LIKE + SHOWS AN ERROR "IS NOT PERSISTEN WITHIN THIS SESSION" ###
@router.delete("/posts/{id}/like")
def unlike_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
            
            post = db.query(models.Post).filter(models.Post.id == id).first()
            
            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"post with id: {id} was not found.")
                
            # if post.owner_id == current_user.id:
            #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

    # we will check if the user has already liked the post or not:  
            like = db.query(models.Like).filter(models.Like.post_id == id, models.Like.user_id == current_user.id).first()

            if not like:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

            db.delete(like)
            db.commit()
            db.refresh(like)

            return like

# get all the likes of a post:
@router.get("/posts/{id}/like")
def get_likes(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
                
                post = db.query(models.Post).filter(models.Post.id == id).first()
                
                if not post:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"post with id: {id} was not found.")
                    
                if post.owner_id == current_user.id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

                

                likes = db.query(models.Like).filter(models.Like.post_id == id).all()

                return likes




# get all the posts that a user has liked:    ##### NOT WORKING PROPERLY -- UNPROCESSABLE ENTITY #####
@router.get("/posts/liked")
def get_liked_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
                
                posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
                
                if not posts:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"post with id: {id} was not found.")
                    
                # if post.owner_id == current_user.id:
                #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

                

                likes = db.query(models.Like).filter(models.Like.user_id == current_user.id).all()

                return likes





# give a dislike to a post:
@router.post("/posts/{id}/dislike")
def dislike_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
            
            post = db.query(models.Post).filter(models.Post.id == id).first()
            
            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"post with id: {id} was not found.")
                
            # if post.owner_id == current_user.id:
            #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

            # check if the user has already disliked the post or not:
            if db.query(models.Dislike).filter(models.Dislike.post_id == id, models.Dislike.user_id == current_user.id).first():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

            dislike = models.Dislike(user_id = current_user.id, post_id = id)
            db.add(dislike)
            db.commit()
            db.refresh(dislike)

            return dislike

# undislike a post:
@router.delete("/posts/{id}/dislike")
def undislike_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
                    
                    ## Getting "is not persistent" error here: ## 


                    post = db.query(models.Post).filter(models.Post.id == id).first()
                    
                    if not post:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f"post with id: {id} was not found.")
                        
                    if post.owner_id == current_user.id:
                        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )        

                    dislike = db.query(models.Dislike).filter(models.Dislike.post_id == id, models.Dislike.user_id == current_user.id).first()

                    if not dislike:
                        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )

                    db.delete(dislike)
                    db.commit()
                    db.refresh(dislike)

                    return dislike




# get all the dislikes of a post:
@router.get("/posts/{id}/dislike")
def get_dislikes(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
                            
                            post = db.query(models.Post).filter(models.Post.id == id).first()
                            
                            if not post:
                                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                    detail=f"post with id: {id} was not found.")
                                
                            if post.owner_id == current_user.id:
                                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
                            
    
                            dislikes = db.query(models.Dislike).filter(models.Dislike.post_id == id).all()
    
                            return dislikes

# get all the posts that a user has disliked:
@router.get("/posts/disliked")
def get_disliked_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
                                    
                                    posts = db.query(models.Post).join(models.Dislike).filter(models.Dislike.user_id == current_user.id).all()
            
                                    return posts


# get all likes and dislikes of a post:
@router.get("/posts/{id}/likes")
def get_likes_dislikes(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
                                            
                                            post = db.query(models.Post).filter(models.Post.id == id).first()
                                            
                                            if not post:
                                                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                                    detail=f"post with id: {id} was not found.")
                                                
                                            # if post.owner_id == current_user.id:
                                            #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
            
                                            # get the count of likes and dislikes:
                                            likes_count = db.query(models.Like).filter(models.Like.post_id == id).count()
                                            dislikes_count = db.query(models.Dislike).filter(models.Dislike.post_id == id).count()


                                            # THIS PART IS ONLY NECESSARY IF WE WANT TO GET THE USERS WHO LIKED AND DISLIKED THE POST:
                                            #likes = db.query(models.Like).filter(models.Like.post_id == id).all()
                                            #dislikes = db.query(models.Dislike).filter(models.Dislike.post_id == id).all()
            
                                            #return {"likes":likes,"dislikes":dislikes,"likes_count":likes_count,"dislikes_count":dislikes_count}   
                                            return {"likes_count":likes_count,"dislikes_count":dislikes_count}  

                                    