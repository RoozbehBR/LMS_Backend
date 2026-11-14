from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import users, courses, enrollments


@asynccontextmanager
async def lifespan(app: FastAPI):
    # این تابع موقع روشن شدن سرور اجرا می‌شه و جدول‌ها رو توی دیتابیس می‌سازه
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="LMS API",
    description="سیستم مدیریت آموزش با رابطه چند‌به‌چند",
    version="0.1.0",
    lifespan=lifespan,
)

# وصل کردن هر سه روتر به اپلیکیشن اصلی با پیشوند /api/v1
app.include_router(users.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(enrollments.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}