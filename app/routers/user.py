from fastapi import Depends, HTTPException, status, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

# Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def creat_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hashing password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) #unpack the user detaills & save it 
    db.add(new_user) # add to the DB
    db.commit() # save it
    db.refresh(new_user) # save the user detaills from the db to new_post

    return new_user
    
#Get User
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"user with id: {id} Not found")
    
    return user
