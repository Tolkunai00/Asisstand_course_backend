from my_site.db.models import Enrollment, UserProfile, StudyGroup
from my_site.db.schema import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
from my_site.db.database import SessionLocal

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List


enrollment_router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollment CRUD"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@enrollment_router.post("/", response_model=EnrollmentResponse)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    student_db = db.query(UserProfile).filter(
        UserProfile.id == enrollment.student_id
    ).first()

    if not student_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай студент жок"
        )

    group_db = db.query(StudyGroup).filter(
        StudyGroup.id == enrollment.group_id
    ).first()

    if not group_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай группа жок"
        )

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        group_id=enrollment.group_id,
        status_enrollment=enrollment.status_enrollment
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


@enrollment_router.get("/", response_model=List[EnrollmentResponse])
async def list_enrollments(
    db: Session = Depends(get_db)
):
    return db.query(Enrollment).all()


@enrollment_router.get(
    "/{enrollment_id}",
    response_model=EnrollmentResponse
)
async def detail_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    enrollment_db = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id
    ).first()

    if not enrollment_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай enrollment жок"
        )

    return enrollment_db


@enrollment_router.put(
    "/{enrollment_id}",
    response_model=EnrollmentResponse
)
async def update_enrollment(
    enrollment_id: int,
    enrollment: EnrollmentUpdate,
    db: Session = Depends(get_db)
):
    enrollment_db = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id
    ).first()

    if not enrollment_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай enrollment жок"
        )

    if enrollment.student_id is not None:
        student_db = db.query(UserProfile).filter(
            UserProfile.id == enrollment.student_id
        ).first()

        if not student_db:
            raise HTTPException(
                status_code=404,
                detail="Мындай студент жок"
            )

    if enrollment.group_id is not None:
        group_db = db.query(StudyGroup).filter(
            StudyGroup.id == enrollment.group_id
        ).first()

        if not group_db:
            raise HTTPException(
                status_code=404,
                detail="Мындай группа жок"
            )

    update_data = enrollment.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(enrollment_db, field, value)

    db.commit()
    db.refresh(enrollment_db)

    return enrollment_db


@enrollment_router.delete(
    "/{enrollment_id}",
    response_model=dict
)
async def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    enrollment_db = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id
    ).first()

    if not enrollment_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай enrollment жок"
        )

    db.delete(enrollment_db)
    db.commit()

    return {
        "message": "Enrollment өчүрүлдү"
    }