from urllib import response
from app import models, utils
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from fastapi import status,Depends,HTTPException,Response,APIRouter
from app import schemas, oauth2
from sqlalchemy.orm import Session
from app.models import Post



router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model = schemas.Token)
def login(user_login:OAuth2PasswordRequestForm = Depends(),db:Session =Depends(get_db)):
    user =db.query(models.User).filter(models.User.email==user_login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    user_verify = utils.verify(user_login.password, user.password)
    if not user_verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    access_token =oauth2.create_access_token(data={'user_id':user.id})
    return {"access_token":access_token, "token_type":"bearer_token"}