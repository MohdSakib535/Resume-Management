from fastapi import APIRouter,Depends,status
from app.database.schema import ResumeBase,ResumeCreate,UserBase,ResumeDetail,ResumeInDB,ResumeList,ResumeExperiences,ResumeEducation,ResumeUpdate,ResumeSearchRequest
from app.database.session import get_db
from app.views.resume_view import create_resume_view,get_all_resume_view,resume_skills_view,resume_experiences_view,resume_educations_view,update_resume_view,search_resumes_view,delete_resume_view
from app.core.utils import get_current_user
from typing import List

resume_router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

OAUTH_CURRENT_USER=Depends(get_current_user)

@resume_router.post("/create",status_code=status.HTTP_201_CREATED)
def create_resume(request:ResumeCreate,db=Depends(get_db),current_user:UserBase = OAUTH_CURRENT_USER):
    print('user--------',current_user)
    return create_resume_view(request,db,current_user)



# Update Resume Route
@resume_router.put("/update/{resume_id}", status_code=status.HTTP_200_OK, response_model=ResumeUpdate)
def update_resume(resume_id: int, request: ResumeUpdate, db = Depends(get_db), current_user: UserBase = OAUTH_CURRENT_USER):
    return update_resume_view(resume_id, request, db, current_user)


#delete resume route
@resume_router.delete("/delete/{resume_id}", status_code=status.HTTP_200_OK)
def delete_resume(
    resume_id: int,
    db = Depends(get_db),
    current_user: UserBase = OAUTH_CURRENT_USER  
):
    return delete_resume_view(resume_id, db, current_user)





@resume_router.get("/all-details",status_code =status.HTTP_200_OK,response_model=List[ResumeDetail])
# def get_all_resume(db = Depends(get_db),current_user:UserBase = OAUTH_CURRENT_USER):
def get_all_resume(db = Depends(get_db)):
    return get_all_resume_view(db)


@resume_router.get('/skills',status_code=status.HTTP_200_OK)
def get_resume_skills(db=Depends(get_db)):
    return resume_skills_view(db)


@resume_router.get('/experience',status_code=status.HTTP_200_OK,response_model=List[ResumeExperiences])
def get_resume_experiences(db=Depends(get_db)):
    return resume_experiences_view(db)



@resume_router.get('/education',status_code=status.HTTP_200_OK,response_model=List[ResumeEducation])
def get_resume_education(db=Depends(get_db)):
    return resume_educations_view(db)


@resume_router.get("/search", status_code=status.HTTP_200_OK, response_model=list[ResumeDetail])
def search_resumes(
    filters: ResumeSearchRequest = Depends(),
    db= Depends(get_db)
):
    return search_resumes_view(db, filters)