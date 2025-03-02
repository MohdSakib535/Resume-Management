from sqlalchemy import Column, Integer, String, ForeignKey, Text,DateTime,JSON,Table,Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime
from sqlalchemy.sql import func


resume_skills = Table(
    'resume_skills',
    Base.metadata,
    Column('resume_id', Integer, ForeignKey('resumes.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)




class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    """Resume model linked to a User"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    phone = Column(String(20))
    linkedin_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="resumes")
    educations = relationship("Education", back_populates="resume", cascade="all, delete-orphan")
    experiences = relationship("WorkExperience", back_populates="resume", cascade="all, delete-orphan")
    skills = relationship("Skill", secondary=resume_skills, back_populates="resumes")

class Education(Base):
    """Education details linked to a Resume"""
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    degree = Column(String(100), nullable=False)
    institution = Column(String(100), nullable=False)
    year_start = Column(Integer)
    year_end = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    resume = relationship("Resume", back_populates="educations")

class WorkExperience(Base):
    """Work experience linked to a Resume"""
    __tablename__ = "work_experiences"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    year_start = Column(Integer)
    year_end = Column(Integer, nullable=True)
    current = Column(Boolean, default=False)
    achievements = Column(Text, nullable=True)

    resume = relationship("Resume", back_populates="experiences")

class Skill(Base):
    """Skill model for Many-to-Many Resume relationship"""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    
    resumes = relationship("Resume", secondary=resume_skills, back_populates="skills")



