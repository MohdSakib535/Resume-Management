from app.database.models import Resume,WorkExperience,Education,Skill
from app.database.schema import ResumeBase,ResumeCreate,UserBase,ResumeUpdate,ResumeList,ResumeSearchRequest,Skill_data
from app.database.session import get_db
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException

# --------------------------------create resume data---------------------
"""
{
  "full_name": "Mohd Sakib",
  "phone": 1234567890,
  "linkedin_url": "https://linkedin.com/in/mohdsakib",
  "educations": [
    {
      "degree": "Bachelor of Technology",
      "institution": "Indian Institute of Technology",
      "year_start": 2015,
      "year_end": 2019,
      "description": "Studied Computer Science and Engineering with a focus on AI and ML."
    },
    {
      "degree": "Master of Science",
      "institution": "Stanford University",
      "year_start": 2020,
      "year_end": 2022,
      "description": "Specialized in Software Engineering and Cloud Computing."
    }
  ],
  "experiences": [
    {
      "company": "Google",
      "role": "Software Engineer",
      "year_start": 2022,
      "year_end": null,
      "current": true,
      "achievements": "Developed scalable microservices and optimized cloud-based applications."
    },
    {
      "company": "Microsoft",
      "role": "Backend Developer",
      "year_start": 2020,
      "year_end": 2022,
      "current": false,
      "achievements": "Implemented REST APIs for enterprise applications and improved system performance."
    },
    {
      "company": "Amazon",
      "role": "Intern - Software Engineer",
      "year_start": 2019,
      "year_end": 2020,
      "current": false,
      "achievements": "Worked on AWS Lambda functions and automated deployment pipelines."
    }
  ],
  "skills": [
    "Python",
    "Django",
    "FastAPI",
    "PostgreSQL",
    "Docker"
  ]
}
"""

def create_resume_view(request: ResumeBase,db: Session,current_user: UserBase):
    linkedin_url_str = str(request.linkedin_url) if request.linkedin_url else None

    new_resume = Resume(
        full_name=request.full_name,
        phone=request.phone,
        email=current_user.email,
        linkedin_url=linkedin_url_str,
        user_id=current_user.id
        )
    
    db.add(new_resume)
    db.flush()


    # Add Educations
    for edu in request.educations:
        education = Education(
            resume_id=new_resume.id,
            degree=edu.degree,
            institution=edu.institution,
            year_start=edu.year_start,
            year_end=edu.year_end,
            description=edu.description
        )
        db.add(education)

    # Add Work Experiences
    for exp in request.experiences:
        experience = WorkExperience(
            resume_id=new_resume.id,
            company=exp.company,
            role=exp.role,
            year_start=exp.year_start,
            year_end=exp.year_end,
            current=exp.current,
            achievements=exp.achievements
        )
        db.add(experience)

    # Add Skills (many-to-many)
    for skill_name in request.skills:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if not skill:
            skill = Skill(name=skill_name) 
            db.add(skill)
            db.flush()
        new_resume.skills.append(skill)

    db.commit()
    db.refresh(new_resume)
    return new_resume


#--------------------- update resume data---------------------------


"""
{
  "full_name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "+1234567890",
  "linkedin_url": "https://www.linkedin.com/in/johndoe",
  "educations": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "XYZ University",
      "year_start": 2015,
      "year_end": 2019,
      "description": "Focused on software development and AI research."
    }
  ],
  "experiences": [
    {
      "company": "TechCorp",
      "role": "Software Engineer",
      "year_start": 2020,
      "year_end": 2023,
      "current": false,
      "achievements": "Developed a scalable microservices architecture."
    }
  ],
  "skills": [
    {"id": 7, "name": "Python"},
    {"id": 10, "name": "FastAPI"},
    {"id": 15, "name": "Docker"}
  ]
}
"""


def update_resume_view(resume_id: int, request: ResumeUpdate, db: Session, current_user: UserBase):
    existing_resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()

    if not existing_resume:
        raise HTTPException(status_code=404, detail="Resume not found or you don't have permission to update it.")

    linkedin_url_str = str(request.linkedin_url) if request.linkedin_url else existing_resume.linkedin_url

    # Update Fields
    existing_resume.full_name = request.full_name if request.full_name else existing_resume.full_name
    existing_resume.phone = request.phone if request.phone else existing_resume.phone
    existing_resume.linkedin_url = linkedin_url_str

    # Update Educations
    if request.educations is not None:
        db.query(Education).filter(Education.resume_id == resume_id).delete()
        for edu in request.educations:
            new_edu = Education(
                resume_id=resume_id,
                degree=edu.degree,
                institution=edu.institution,
                year_start=edu.year_start,
                year_end=edu.year_end,
                description=edu.description
            )
            db.add(new_edu)

    # Update Work Experiences
    if request.experiences is not None:
        db.query(WorkExperience).filter(WorkExperience.resume_id == resume_id).delete()
        for exp in request.experiences:
            new_exp = WorkExperience(
                resume_id=resume_id,
                company=exp.company,
                role=exp.role,
                year_start=exp.year_start,
                year_end=exp.year_end,
                current=exp.current,
                achievements=exp.achievements
            )
            db.add(new_exp)

    # Update Skills (Many-to-Many)
    if request.skills is not None:
        existing_resume.skills.clear() 
        for skill in request.skills:
            # Extract skill name from Skill_data object if necessary
            skill_name = skill.name if isinstance(skill, (Skill, Skill_data)) else skill  

            existing_skill = db.query(Skill).filter(Skill.name == skill_name).first()
            
            if not existing_skill:
                new_skill = Skill(name=skill_name)
                db.add(new_skill)
                db.flush()
                existing_resume.skills.append(new_skill)
            else:
                existing_resume.skills.append(existing_skill)

    db.commit()
    db.refresh(existing_resume)
    return existing_resume





def delete_resume_view(resume_id: int, db: Session, current_user: UserBase):
    # Check if the resume exists
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    #Ensure the logged-in user owns the resume
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own resume")

    #  Delete resume 
    db.delete(resume)
    db.commit()

    return {"message": "Resume deleted successfully"}






def get_all_resume_view(db: Session):
    resumes = (
            db.query(Resume)
            .options(
                joinedload(Resume.user),        
                joinedload(Resume.educations),  
                joinedload(Resume.experiences), 
                joinedload(Resume.skills)     
            )
            .all()
        )

    return resumes


def resume_experiences_view(db:Session):
    resume_dta=db.query(Resume).all()
    return resume_dta


def resume_educations_view(db:Session):
    # resume_dta=db.query(Resume).all()
    resume_dta = db.query(Resume).options(joinedload(Resume.educations)).all()
    return resume_dta


def resume_skills_view(db:Session):
    # resume_dta=db.query(Resume).all()
    resume_dta=db.query(Resume).options(joinedload(Resume.skills)).all()  #optimized using joint
    
    resume_list = []
    for resume in resume_dta:
        resume_list.append({
            "id": resume.id,
            "full_name": resume.full_name,
            "email": resume.email,
            "phone": resume.phone,
            "linkedin_url": resume.linkedin_url,
            "created_at": resume.created_at,
            "updated_at": resume.updated_at,
            "skills": [skill.name for skill in resume.skills]  
        })

    return resume_list



def search_resumes_view(db: Session, filters: ResumeSearchRequest):
    query = db.query(Resume)
    filters_applied = False 

    #  Filter by Skill
    if filters.skill:
        query = query.join(Resume.skills).filter(Skill.name.ilike(f"%{filters.skill}%"))
        filters_applied = True

    #  Filter by Education Degree
    if filters.degree:
        query = query.join(Resume.educations).filter(Education.degree.ilike(f"%{filters.degree}%"))
        filters_applied = True

    # Filter by Work Experience Company
    if filters.company:
        query = query.join(Resume.experiences).filter(WorkExperience.company.ilike(f"%{filters.company}%"))
        filters_applied = True

    #  Filter by Job Role
    if filters.role:
        query = query.join(Resume.experiences).filter(WorkExperience.role.ilike(f"%{filters.role}%"))
        filters_applied = True

    #  Filter by User Email
    if filters.email:
        query = query.join(Resume.user).filter(Resume.user.has(email=filters.email))
        filters_applied = True

    #  Filter by End Year in Education or Work Experience
    if filters.end_year:
        query = query.outerjoin(Resume.educations).outerjoin(Resume.experiences).filter(
            (Education.year_end == filters.end_year) | (WorkExperience.year_end == filters.end_year)
        )
        filters_applied = True

    resumes = query.all()

    #  If filters were used but no data found, return 404 response
    if filters_applied and not resumes:
        raise HTTPException(status_code=404, detail="No data found matching the filters")

    return resumes