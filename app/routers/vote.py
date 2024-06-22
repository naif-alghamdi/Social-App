from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, db, models, oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(db.get_db), current_user: int =  Depends(oauth2.get_current_user)):

    post = db.query(models.posts).filter(models.posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} not found")

    vote_quiry = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_quiry.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has alrady voted this post {vote.post_id}")
        
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()

        return {"msg": "successfull added vote"}
    else:
        if not vote_quiry:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote dose not exsit")
        
        vote_quiry.delete(synchronize_session=False)
        db.commit()

        return {"msg": "succsflly deleted vote"}