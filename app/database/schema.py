from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator, ConfigDict,Field
from datetime import datetime



"-------------------education schema------------------"
# Education schemas
class EducationBase(BaseModel):
    degree: str
    institution: str
    year_start: int
    year_end: int | None = None
    description: str | None = None

    class Config:
        from_attributes = True

    @field_validator('year_end')
    @classmethod
    def validate_year_end(cls, v, values):
        print('value-----',values.data.get('year_start'))
        if v is not None and v < values.data.get('year_start', 0):
            raise ValueError("Year end must be greater than or equal to year start")
        return v

class EducationCreate(EducationBase):
    pass

class EducationUpdate(EducationBase):
    degree: str | None = None
    institution: str | None = None
    year_start: int | None = None

class Education(EducationBase):
    id: int
    resume_id: int

    model_config = ConfigDict(from_attributes=True)



"--------------------experience schema-------------------"
# Work Experience schemas
class WorkExperienceBase(BaseModel):
    company: str
    role: str
    year_start: int
    year_end: int | None = None
    current: bool = False
    achievements: str | None = None

    class Config:
        from_attributes = True

    @field_validator('year_end')
    @classmethod
    def validate_year_end(cls, v, values):
        if v is not None and v < values.data.get('year_start', 0):
            raise ValueError("Year end must be greater than or equal to year start")
        if values.data.get('current', False) and v is not None:
            raise ValueError("If current is True, year_end must be None")
        return v

class WorkExperienceCreate(WorkExperienceBase):
    pass

class WorkExperienceUpdate(WorkExperienceBase):
    company: str | None = None
    role: str | None = None
    year_start: int | None = None

class WorkExperience(WorkExperienceBase):
    id: int
    resume_id: int

    model_config = ConfigDict(from_attributes=True)




"------------skills schema--------------------"

# Skill schemas
class SkillBase(BaseModel):
    name: str

class SkillCreate(SkillBase):
    pass

class Skill_data(SkillBase):
    id: int

    class Config:
        from_attributes = True



"-----------------------Resume schemas-----------------"

class ResumeBase(BaseModel):
    full_name: str
    phone: str
    linkedin_url: HttpUrl | None = None

class ResumeCreate(ResumeBase):
    educations: List[EducationCreate]
    experiences: List[WorkExperienceCreate]
    skills: List[str]  # Only skill names

class ResumeUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    linkedin_url: HttpUrl | None = None
    educations: List[EducationCreate] | None = None
    experiences: List[WorkExperienceCreate] | None = None
    skills: List[Skill_data] | None = None

class ResumeList(ResumeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    skills: List[str]


class resumeUser(BaseModel):
    username:str
    email:str
    # class Config:
    #     orm_mode = True

class ResumeInDB(ResumeBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    
    class Config:
      from_attributes = True

class ResumeList(ResumeInDB):
    skills: List[str]  # Just skill names for the list view


class ResumeExperiences(ResumeInDB):
    experiences:List[WorkExperienceBase]

class ResumeEducation(ResumeInDB):
    educations:List[EducationBase]

class ResumeDetail(ResumeInDB):
    user:resumeUser
    educations: List[Education]
    experiences: List[WorkExperience]
    skills: List[Skill_data]

# Pagination
class PaginatedResponse(BaseModel):
    items: List[ResumeList]
    total: int
    page: int
    size: int
    pages: int






"-----------token -------------------"

from typing import Optional
from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # username: str | None = None
    email: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str
    password:str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)








class ResumeSearchRequest(BaseModel):
    skill: Optional[str] = Field(None, description="Filter by skill name")
    degree: Optional[str] = Field(None, description="Filter by education degree")
    company: Optional[str] = Field(None, description="Filter by work experience company")
    role: Optional[str] = Field(None, description="Filter by job role in work experience")
    email: Optional[EmailStr] = Field(None, description="Filter by user's email")
    end_year: Optional[int] = Field(None, description="Filter by year_end in education or work experience")