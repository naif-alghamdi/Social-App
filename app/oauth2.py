from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, db, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str):

    credantials_excption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="cant valdate cerdantails", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credantials_excption

        token_data = schemas.TokenData(id=str(id))

    except JWTError:
        raise credantials_excption
    #print(token_data)
    return token_data # return id from token after validating
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)):

    token = verify_access_token(token)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    print(user)
    return user