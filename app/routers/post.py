from typing import List, Optional
from app.database import get_db
from sqlalchemy import func
from app import oauth2
from fastapi import status,Depends,HTTPException,Response,APIRouter
from app import schemas
from sqlalchemy.orm import Session
from app.models import Post, User, Vote



router =APIRouter(
    prefix="/posts",
     tags=['Posts']
)

@router.get("/",
#  response_model=List[schemas.ShowPost]
 )
def get_posts(
    db: Session = Depends(get_db),
    limit:int =10,
    skip:int =0,
    search:Optional[str] = "",
     current_user =Depends(oauth2.get_current_user)
     ):
    results =db.query(Post,func.count(Vote.post_id).label("votes")).join(Vote, Post.id==Vote.post_id, isouter=True).group_by(Post.id).filter(Post.title.contains(search)).limit(limit).offset(skip).all()

    return  results


@router.get("/{id}", 
# response_model=schemas.Post
)
def get_post(
    id: int,
 db: Session = Depends(get_db),
  current_user:int =Depends(oauth2.get_current_user)
  ):
    post = db.query(Post,func.count(Vote.post_id).label("votes")).join(Vote, Post.id==Vote.post_id, isouter=True).group_by(Post.id).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    return  post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
     db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
    ):
    
    new_post = Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post







@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(
    id: int,
     update_post: schemas.PostCreate,
     db: Session = Depends(get_db),
      current_user = Depends(oauth2.get_current_user)
      ):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(update_post.dict())
    db.commit()
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
 current_user =Depends(oauth2.get_current_user)
 ):

    post_query = db.query(Post).filter(Post.id == id)
    post =post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)