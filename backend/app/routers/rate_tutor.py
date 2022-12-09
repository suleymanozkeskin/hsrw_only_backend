from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models,oauth2
router = APIRouter(tags=["Rate Tutor"] )


# @router.post("/rate_tutor", status_code = status.HTTP_201_CREATED)
# def rate(profile: schemas.RateTutor2 , db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
#     rate_list =[1,2,3,4,5,6,7,8,9,10]
    
#     # so if we wanna make a vote, we will check whether there is an already existing vote or not.
#     # then we are gonna filter by Vote.post_id and see if there is already a vote for this  specific post_id 
#     # however this is not enough because multiple people can vote on the same post
#     # so we have to do a second check: models.Vote.user_id == current_user.id
    
#     profile = db.query(models.Be_Tutor).filter(models.Be_Tutor.id == rate.tutor_profile_id).first() # We are gonna take query the post and if the post does not exist , user can not vote on it.
#     if not profile:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile with id: {rate.tutor_profile_id} does not exist.")
     
    
#     rate_query = db.query(models.Rating_Tutor).filter(models.Rating_Tutor.post_id == rate.post_id, models.Rating_Tutor.user_id == current_user.id)
    
#     found_rate = rate_query.first()
    
#     if found_rate in rate_list:
        
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {rate.post_id} .")
        
#     new_rate = models.Rating_Tutor(profile_id = rate.profile_id, user_id = current_user.id)
        
        
#     db.add(new_rate)
#     db.commit()
#     return{"message": "successfully added vote"}   
            
   
   
@router.post("/rate_tutor/{id}",status_code=status.HTTP_201_CREATED)
def rate(id: int,rate: schemas.RateTutor, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    
 
    
    # We are gonna check if this specific user has already rated this specific profile
    #rate_query= db.query(models.Rating_Tutor).filter(models.Be_Tutor.id == id,models.Rating_Tutor.user_email == current_user.email).first()

    #found_rate = rate_query.first()

      
    #new_post = models.Post(owner_id=current_user.id,  **post.dict()) ## this method will take the post as dictionary and automatically import it from there as opposed to manual typing version below:
    # new_post = models.Post(title=post.title, content=post.content , published= post.published)  
        
    print("Hello World")
    # if rate_query:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"user with the following email address: {current_user.email} has already rated this tutor profile ")
    print('___')
    print(id) # id ✅
    print('___') #
    print(current_user.email) # <app.models.User object at 0x7f27b6a91670> Ali.Geyik@hsrw.org
    print('___')
    print(rate.RatingScore) # 2 puan ✅
    print('___')

    new_rate = models.Rating_Tutor(user_email = current_user.email,tutor_profile_id = id , RatingScore = rate.RatingScore)
    
    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)

    return new_rate

    # if not rate_query:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Rate does not exist.")
    
    # rate_query.delete(synchronize_session=False)
    # db.commit()
    # return{"Successfully deleted rate."}        
            
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    # print(rate)
    # print(type(rate))
    
    
    # rate_query = db.query(models.Rating_Tutor).filter(models.Rating_Tutor.post_id == rate.post_id, models.Rating_Tutor.user_id == current_user.id)
    
    # found_rate = rate_query.first()
    
    # db.add(new_rate)
    # db.commit()
    # return{"message": "successfully added vote"}   
    
    
    # if rate in rate_list:
    #     db.query(models.Rating_Tutor).filter(models.Rating_Tutor.RatingID == rate.user_id, models.Rating_Tutor.user_id == current_user.id)
        
        
        
    # else:
    #     return {"message": " Your rate cannot exceed the range of 1-10."}
        