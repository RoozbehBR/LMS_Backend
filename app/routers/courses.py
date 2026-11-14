from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_course, get_course, get_courses
from app.database import get_db
from app.schemas import CourseCreate, CourseResponse


router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=CourseResponse, status_code=http_status.HTTP_201_CREATED)
async def create_new_course(data: CourseCreate, db: AsyncSession= Depends(get_db)):
  return await create_course(db, data)

@router.get("/",response_model= list[CourseResponse])
async def list_courses(db: AsyncSession= Depends(get_db)):
  return await get_courses(db)

@router.get("/{course_id}", response_model= CourseResponse)
async def read_course(course_id: int, db: AsyncSession= Depends(get_db)):
  course = await get_course(db,course_id)
  if not course:
    raise HTTPException(status_code=404, detail= "Course not found !")
  return course