# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time 
from fastapi import FastAPI
from . import models 
from .database import engine
from .routers import post,user, auth, vote 
from .config import settings 
from fastapi.middleware.cors import CORSMiddleware 

models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {'message':"Hello Divyang FastAPI1"}
 

# it is refer as schema it is called pydantic model and another Post inside model file Post  it is called sqlAlchemy model for table in DB 
# Schema or pydantoc model is used for API when inside routes file we are passing functions as in argument of functions 
# we are passing the schemas or pydantoc model as argument when we call the functions as per routes 
# schema/pydantic models define the structure of request response.
# This ensures that when a user wants to create a post, request will only goes if it has title and content in the body.
# so pydantic model perform little validation should we crete a brand new post 

# other model is SQLAlchemy model inside models.py file and this are responsible for defining the columns for in our postgres DB.
# we used to CRUD operation over it table so for table in DB we have SQLAlchemy model. and for database whcih fields should be there which table should
# be there table name which is null which is notnull which is by default all things comes under SQLAlchemy model for DB 
# so schemas.py is for api request response and Sqlalchemy model is for DB databse table and all  
# so here in schemas we use pydantic model so in pydantic model. pydantic model for request response we have defined inside inside schemas.py 
# SQLAlchemy models are inside models.py 

# Technically we dont need pydantic model but when it comes to build API's you want to build strict as possible when it comes to what kind of data 
# can we receive and send to the user. so pydantic model and ORM model two models are there for API reqest response there is pydantic model and for DB its ORM Sqlalchemy model


# class Post(BaseModel):
#     title:str 
#     content:str
#     published:bool = True

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi_fcc',
#             user='postgres',
#             password='your_new_password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print(f"Error: {error}")
#         time.sleep(2)


# my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
#               {"title": "title of post 2", 'content': 'content of post 2', 'id': 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

#     return None

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

#     return None


#here after adding router we have to do uvicorn app.main:app --reload --port 8000 this makes whichever files inside auth.py or post.py or user.py 
# can be imported because this file is created inside __pycache__ folder as inside this folder it should be created if its not created we can not import 
# directly like from .router import auth for that we have reload uvicorn app 

 





 
    