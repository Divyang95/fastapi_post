from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session 
from .. import models,schemas,oauth2
from ..database import get_db
from typing import List, Optional 
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)


# @router.get('/',response_model=List[schemas.Post]) 
@router.get('/',response_model=List[schemas.PostOut]) 
def get_posts(db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user), limit:int=10,
               skip:int=0, search: Optional[str]=''):
    print(limit)
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(posts) 
     
    posts = (db.query(models.Post, func.count(models.Vote.post_id).label('votes')
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id
                       ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())
    print(posts)


    return results
    # return [{"Post": post, "LIKES": likes} for post, likes in results]

# by using response model as pydantic model we can send only data whatever we want to pass so whichever fields are defined inside pydantic model 
# only that model fields are come as respone so pydantic model is used for both req and response 
# as below for creating post also we have passed pydantic model so that fields should be there in body and type should be as per model 

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # here we have imported schemas because we have two Post model one is pydantic and another is ORM or Sqlalchemy so when we want to call
    # pydantic model we do schemas.Post and we want ORM model SQLAlchemy model we do models.Post
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    new_post=models.Post(owner_id=current_user.id ,**post.dict()) #its a ORM model or SQLAlchemy model 
    db.add(new_post) #changes in transaction
    db.commit() #changes in actual DB
    db.refresh(new_post) #fetch data from DB 

    return new_post
# so we have lotof power and flexibility on what to provide as response if we use pydantic model as response  
# here we have protected /post end point so whenever this create_post function user try to call we check first that token validation 
# get_current_user function which gives id of user and checks token and verify it with secret during each createpost function call
# current_user:int=Depends(oauth2.get_current_user) by using this we can confirm that user is logged in so pass it to every function


@router.get('/{id}',response_model=schemas.PostOut )
def get_post(id:int,db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first() 

    post=(db.query(models.Post, func.count(models.Vote.post_id).label('votes')
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id
                       )).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.first().owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False) #no need to load row in memory so no need to apply first() or all(). we can delete directly in DB.
    #same method we are applying to update directly in DB.we dont take db row in memory.
    # but for when user wants see single post or multiple post we can use .all and .first on it save it to memory and 
    # directly saved memory is that posts are returned 
    db.commit()
    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate,db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_db = post_query.first()

    if post_db is None:       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post_db.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()