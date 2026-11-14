from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_enrollment, get_user_enrollments
from app.database import get_db
from app.schemas import EnrollmentCreate, EnrollmentResponse

router = APIRouter(tags=["Enrollments"])

@router.post("/users/{user_id}/enrollments/", response_model=EnrollmentResponse, status_code=http_status.HTTP_201_CREATED)
async def enroll_user_in_course(user_id: int, data: EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_enrollment(db, user_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}/enrollments/", response_model=list[EnrollmentResponse])
async def read_user_enrollments(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_enrollments(db, user_id)