from my_site.db.models import Application, UserProfile, Course
from my_site.db.schema import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from my_site.db.database import SessionLocal

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List


application_router = APIRouter(prefix="/applications", tags=["Application CRUD"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application_router.post("/", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    student_db = db.query(UserProfile).filter(UserProfile.id == application.student_id).first()
    if not student_db:
        raise HTTPException(status_code=404, detail="Мындай студент жок")
    course_db = db.query(Course).filter(Course.id == application.course_id).first()
    if not course_db:
        raise HTTPException(status_code=404, detail="Мындай курс жок")
    manager_db = db.query(UserProfile).filter(UserProfile.id == application.manager_id).first()
    if not manager_db:
        raise HTTPException(status_code=404, detail="Мындай менеджер жок")

    new_application = Application(
        student_id=application.student_id,
        course_id=application.course_id,
        manager_id=application.manager_id,
        comment=application.comment,
        status_application=application.status_application
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@application_router.get("/", response_model=List[ApplicationResponse])
async def list_applications(
    db: Session = Depends(get_db)
):
    return db.query(Application).all()


@application_router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
async def detail_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application_db = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай заявка жок"
        )

    return application_db


@application_router.put(
    "/{application_id}",
    response_model=ApplicationResponse
)
async def update_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    application_db = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай заявка жок"
        )

    if application.student_id is not None:
        student_db = db.query(UserProfile).filter(
            UserProfile.id == application.student_id
        ).first()

        if not student_db:
            raise HTTPException(
                status_code=404,
                detail="Мындай студент жок"
            )

    if application.course_id is not None:
        course_db = db.query(Course).filter(
            Course.id == application.course_id
        ).first()

        if not course_db:
            raise HTTPException(
                status_code=404,
                detail="Мындай курс жок"
            )

    if application.manager_id is not None:
        manager_db = db.query(UserProfile).filter(
            UserProfile.id == application.manager_id
        ).first()

        if not manager_db:
            raise HTTPException(
                status_code=404,
                detail="Мындай менеджер жок"
            )

    update_data = application.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(application_db, field, value)

    db.commit()
    db.refresh(application_db)

    return application_db


@application_router.delete(
    "/{application_id}",
    response_model=dict
)
async def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application_db = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай заявка жок"
        )

    db.delete(application_db)
    db.commit()

    return {
        "message": "Заявка өчүрүлдү"
    }