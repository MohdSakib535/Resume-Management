from fastapi import FastAPI
from app.routing.users import user_router
from app.routing.authentication import auth_router
from app.routing.resume import resume_router

app=FastAPI()


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(resume_router)



