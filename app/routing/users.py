from fastapi import APIRouter,Depends,status
from app.database.models import User
from app.database.schema import UserBase
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.views.user_view import create_user_view,all_users_view,get_user_by_id_view



user_router = APIRouter(
    prefix="/users",
    tags=["users"]

)


@user_router.post("/create",status_code=status.HTTP_201_CREATED)
def Create_user(request: UserBase,db: Session = Depends(get_db)):
    return create_user_view(request,db)


@user_router.get("/all",status_code =status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    return all_users_view(db)


@user_router.get("/{user_id}",status_code =status.HTTP_200_OK,response_model=UserBase)
def get_user_by_id(user_id:int,db: Session = Depends(get_db)):
    return get_user_by_id_view(db,user_id)


    


