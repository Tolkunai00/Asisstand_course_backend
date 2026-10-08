from my_site.db.models import Course, Category
from my_site.db.schema import CourseCreate, CourseUpdate, CourseResponse
from my_site.db.database import SessionLocal

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List


course_router = APIRouter(
    prefix="/courses",
    tags=["Course CRUD"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@course_router.post("/", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    category_db = db.query(Category).filter(
        Category.id == course.category_id
    ).first()

    if not category_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай категория жок"
        )

    new_course = Course(
        course_name=course.course_name,
        category_id=course.category_id,
        descriptions=course.descriptions,
        level=course.level,
        price=course.price,
        duration_weeks=course.duration_weeks,
        is_active=course.is_active,
        status=course.status
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@course_router.get("/", response_model=List[CourseResponse])
async def list_courses(
    db: Session = Depends(get_db)
):
    return db.query(Course).all()


@course_router.get("/{course_id}", response_model=CourseResponse)
async def detail_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course_db = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай курс жок"
        )

    return course_db


@course_router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db)
):
    course_db = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай курс жок"
        )

    if course.category_id is not None:
        category_db = db.query(Category).filter(
            Category.id == course.category_id
        ).first()

        if not category_db:
            raise HTTPException(
                status_code=404,
                detail="Мындай категория жок"
            )

    update_data = course.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(course_db, field, value)

    db.commit()
    db.refresh(course_db)

    return course_db


@course_router.delete("/{course_id}", response_model=dict)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course_db = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай курс жок"
        )

    db.delete(course_db)
    db.commit()

    return {
        "message": "Курс өчүрүлдү"
    }