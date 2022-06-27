from multiprocessing import synchronize
from app import database
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db

from app import models, schemas, utils, oauth2


router =APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post("/",status_code=status.HTTP_201_CREATED)   
def vote(
    vote: schemas.Vote,
     db:Session =Depends(get_db),
     current_user =Depends(oauth2.get_current_user)
     ):
    post_exist = db.query(models.Post).filter(models.post.id == vote.post_id).first()
    vote_query=db.query(models.Vote.post_id == vote.post_id,models.Vote.user_id ==current_user.id )
    
    vote_exists=vote_query.first() 
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exists")

    if(vote.dir ==1):
        if vote_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f" user has already voted on post with id {vote.post_id}")
        new_vote=models.vote(post_id= vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Post successfully voted on"}
    else:
        if not vote_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exists")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote successfully deleted"}



        


