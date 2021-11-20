from fastapi import APIRouter, Depends, params, status , HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import sessionmaker
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from app import oauth2 

from .. import database, schema, models, utils

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session= Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print("User Email : ",user.email, " Use password : ",user.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    print("before token generation")
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    print("after token generation")
    return {"token":access_token, "token_type":"bearer"}
