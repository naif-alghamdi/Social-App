from fastapi import Depends, HTTPException, status, Response, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..db import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#Get All posts
@router.get("/", response_model=List[schemas.PostOut]) #response_model=List[schemas.PostOut]
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # Query the database to retrieve all posts
    # posts = db.query(models.posts).filter(models.posts.owner_id == current_user.id, models.posts.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.posts, func.count(models.Votes.post_id).label("vote")).join(models.Votes, models.posts.id == models.Votes.post_id, isouter=True).group_by(models.posts.id).filter(models.posts.owner_id == current_user.id, models.posts.title.contains(search)).limit(limit).offset(skip).all()

    # results = list(map(lambda x:x._mapping,results)) #for testing
    # Return the retrieved posts
    return results

#Return One POST
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.posts).filter(models.posts.id == current_user.id).first() # save the POTS

    post = db.query(models.posts, func.count(models.Votes.post_id).label("vote")).join(models.Votes, models.posts.id == models.Votes.post_id, isouter=True).group_by(models.posts.id).filter(models.posts.id == id).first()

    if post is None: #Valdation
        raise HTTPException(status_code=404, detail=f"{id} not found") 
    else:
        return post # return POST

#Create Post
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):


    new_post = models.posts(owner_id=current_user.id, **post.dict()) #unpack the post & save it 
    db.add(new_post) # add to the DB
    db.commit() # save it
    db.refresh(new_post) # save the post from the db to new_post
    return new_post

#delete POST
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query = db.query(models.posts).filter(models.posts.id == id) # save post
    post = query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authrized to perfoem requested action")

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update Recored
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query = db.query(models.posts).filter(models.posts.id == id)
    post = query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id: {id} is note found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authrized to perfoem requested action")
    
    query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return query.first()