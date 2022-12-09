from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags=["Users"]
)

## CREATING USERS:

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) ## schemas.UserOut for what to return to user after user creation
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)): ## schemas.UserCreate for creating the user 
   
    # HASH THE PASSWORD: we get user.password from  "user: schemas.UserCreate". Then , we use previously defined pwd_context.hash()  method to hash the user.password.
    #
    hashed_password = utils.hash(user.password)
    user.password = hashed_password         # Here its going to update pydantic user model with the hashed_password
    new_user = models.User(**user.dict())

    exist = db.query(models.User).filter(models.User.email == new_user.email).first()
    if exist != None: 
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                            detail = f"This email: {new_user.email} is already registered.Please use another email or renew your password for this one.") 
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user    
    

@router.get("/users/{id}", response_model=schemas.UserOut)   
def get_user(id: int , db: Session = Depends(get_db)):
    
    user= db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"User with id {id} does not exist.")
    return user
