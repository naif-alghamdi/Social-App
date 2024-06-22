from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import db, schemas, models, utils, oauth2

router = APIRouter(tags=["Authntcation"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user: # check if user esxist in DB
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invaled cerdnatioal")
    
    if not utils.verify(user_credentials.password, user.password): #Check if password match
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invaled cerdnatioal")
    
    access_token = oauth2.create_access_token(data= {"user_id": user.id}) # Genrate Token

    return {"access_token": access_token, "token_type": "bearer"}