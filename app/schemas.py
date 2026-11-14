from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# ۱. قالب‌های کاربر
# ==========================================
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=255)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# ۲. قالب‌های دوره
# ==========================================
class CourseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=2000)

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# ۳. قالب‌های ثبت‌نام (Enrollment)
# ==========================================
class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    course: CourseResponse
    
    model_config = ConfigDict(from_attributes=True)