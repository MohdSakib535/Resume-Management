from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database.models import User
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.core.utils import Hash
from app.core.security import create_access_token,verify_token
# import jwt_token
from app.core.custom_form import OAuth2EmailRequestForm

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/login", )
def login(request: OAuth2EmailRequestForm = Depends(),db:Session=Depends(get_db)):
    user_data=db.query(User).filter(User.email==request.email).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid email or password")
    
    # Verify the password
    if not Hash.verify_user(user_data.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Password")
    
    # Generate the access token
    access_token = create_access_token(data={"sub":user_data.email})
    return {"access_token": access_token, "token_type": "bearer"}



