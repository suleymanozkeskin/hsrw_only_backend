from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import event_post, rate_tutor

from . import models
from .database import engine
from .routers import be_a_tutor, hire_a_tutor, post, user, auth,event_post,rate_tutor
from .config import settings
    






#INTEGRATION OF "models.py" to create database tables: 

models.Base.metadata.create_all(bind=engine)




app = FastAPI()

origins = ["https://www.google.com"]  # this means that currently only google.com can have access to this website but if it were to be a public domain origins would be defined as following:

# origins = ["*"] # public

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
#app.include_router(vote.router)
app.include_router(event_post.router)
app.include_router(be_a_tutor.router)
app.include_router(hire_a_tutor.router)
app.include_router(rate_tutor.router)

@app.get("/")
def root():
    return{"message": "welcome to my page  "}
        
    

## IN ORDER TO START THE APP WE WILL USE THE FOLLOWING:
## uvicorn app.main_3:app --reload
##         app.main_3 specifies that  the  python file called as "main_3.py" within the folder named "app"



#-------------------------------------------------------------------------------------

    
# my_posts = [{"title": "title of post_1 ", "content": "content of post_1", "id": 1},
#             {"title": "title of post_2 ", "content": "content of post_2", "id": 2}]        


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i 




