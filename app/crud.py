from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import User, Course, Enrollment
from app.schemas import UserCreate, CourseCreate, EnrollmentCreate


async def create_user(db: AsyncSession, data: UserCreate)-> User:
  user = User(name= data.name, email= data.email)
  db.add(user)
  await db.commit()
  await db.refresh(user)
  return user

async def get_user(db: AsyncSession, user_id: int)-> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.excute(query)
    return result.scalar_one_or_none()


async def create_course(db: AsyncSession, data: CourseCreate)-> Course:
  course= Course(title= data.title, description= data.descriptionption)
  db.add(course)
  await db.commit()
  await db.refresh(course)
  return course

async def get_course(db: AsyncSession, course_id: int)-> Course | None:
  query = select(Course).where(Course.id == course_id)
  result = await db.excute(query)
  return result.scalar_one_or_none()

async def get_courses(db: AsyncSession)-> list[Course]:
  query = select(Course).order_by(Course.id.desc())
  result = await db.excute(query)
  return list(reslut.scalar().all())


async def get_enrollment(db: AsyncSession, user_id: int, course_id: int) -> Enrollment | None:
    query = select(Enrollment).where(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_enrollment(db: AsyncSession, user_id: int, data: EnrollmentCreate) -> Enrollment:
    # ۱. چک کاربر
    user_check = await get_user(db, user_id)
    if not user_check:
        raise ValueError("کاربر پیدا نشد")

    # ۲. چک دوره
    course_check = await get_course(db, data.course_id)
    if not course_check:
        raise ValueError("دوره پیدا نشد")

    # ۳. چک تکرار (حالا دقیقاً مثل بقیه شد!)
    existing_enrollment = await get_enrollment(db, user_id, data.course_id)
    if existing_enrollment:
        raise ValueError("این کاربر قبلاً در این دوره ثبت‌نام کرده است")

    # ۴. ساخت ثبت‌نام
    enrollment = Enrollment(user_id=user_id, course_id=data.course_id)
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

async def get_user_enrollments(db: AsyncSession, user_id: int) -> list[Enrollment]:
    query = (
        select(Enrollment)
        .where(Enrollment.user_id == user_id)
        .options(selectinload(Enrollment.course))
    )
    result = await db.execute(query)
    return list(result.scalars().all())