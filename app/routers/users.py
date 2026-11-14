from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_user, get_user, create_enrollment, get_user_enrollments
from app.database import get_db
from app.schemas import UserCreate, UserResponse, EnrollmentCreate, EnrollmentResponse

router = APIRouter(prefix="/users", tags=["Users"])

# ۱. ساخت کاربر جدید (اینجا کلمه post درست شد)
@router.post("/", response_model=UserResponse, status_code=http_status.HTTP_201_CREATED)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, data)

# ۲. دیدن اطلاعات یک کاربر خاص
@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")
    return user

# ۳. ثبت‌نام کاربر در یک دوره
@router.post("/{user_id}/enrollments/", response_model=EnrollmentResponse, status_code=http_status.HTTP_201_CREATED)
async def enroll_user(user_id: int, data: EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_enrollment(db, user_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ۴. دیدن دوره‌های ثبت‌نام شده توسط کاربر
@router.get("/{user_id}/enrollments/", response_model=list[EnrollmentResponse])
async def read_user_enrollments(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_enrollments(db, user_id)