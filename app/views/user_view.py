from app.database.models import User
from app.database.schema import UserBase
from sqlalchemy.orm import Session
from app.core import utils as UT
from fastapi import HTTPException, status



def create_user_view(request: UserBase, db: Session):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user = User(username=request.username, 
                    email=request.email, 
                    password=UT.Hash.bcrypt(request.password))
    
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user) 
    return new_user


def all_users_view(db: Session):
    users = db.query(User).order_by(User.id.desc()).all()
    return users


def get_user_by_id_view(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()