from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from app.core.security import  verify_token
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.database.models import User
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash:
    def bcrypt(password: str) ->str:
        hassed_psw = pwd_context.hash(password)
        return hassed_psw
    def verify_user(hashed_password,plain_password):
        data=pwd_context.verify(plain_password,hashed_password)
        return data
    


def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data=verify_token(token, credentials_exception)
    # Query the user from the database using the email from the token
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
   







