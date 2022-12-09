from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.LoginResponse,response_model_exclude={"user.id","user.created_at"})
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):
    
    # #{
    #    "username": "xmen"
    #    "password": "storm"  
    # #}
    
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials.")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials.")
    
    # create a token
    # return a token
    
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
     
    
    return{"access_token": access_token , "token_type": "bearer", "user": user}


## we installed !pip install python-jose[cryptography] for JWT TOKENS.


