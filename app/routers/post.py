from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends , APIRouter
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import func, mode
from ..schema import PostCreate , Post, PostOut, UserLogin
from .. import models
from ..database import  get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from .. import oauth2
router = APIRouter(
    prefix="/posts", 
    tags=['Posts']
)

@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)
,limit:int = 10, skip:int = 0, search: Optional[str]=""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=Post)
def create_posts(post:PostCreate,db: Session = Depends(get_db), current_user:models.User = Depends(get_current_user)): 
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post     


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    return  post 

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not authorised to perform this operation")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=Post)
def update_post(id:int,updated_post:PostCreate, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    update_post = db.query(models.Post).filter(models.Post.id == id)
    post = update_post.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not authorised to perform this operation")
    update_post.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return update_post.first()
