from my_site.db.models import StudyGroup, Course, UserProfile
from my_site.db.schema import StudyGroupCreate, StudyGroupUpdate, StudyGroupResponse
from my_site.db.database import SessionLocal

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List


study_group_router = APIRouter(
    prefix="/study-groups",
    tags=["Study Group CRUD"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@study_group_router.post("/", response_model=StudyGroupResponse)
async def create_study_group(
    study_group: StudyGroupCreate,
    db: Session = Depends(get_db)
):
    course_db = db.query(Course).filter(
        Course.id == study_group.course_id
    ).first()

    if not course_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай курс жок"
        )

    teacher_db = db.query(UserProfile).filter(
        UserProfile.id == study_group.teacher_id
    ).first()

    if not teacher_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай мугалим жок"
        )

    new_study_group = StudyGroup(
        name=study_group.name,
        course_id=study_group.course_id,
        teacher_id=study_group.teacher_id,
        starts_on=study_group.starts_on,
        ends_on=study_group.ends_on,
        status_recruiting=study_group.status_recruiting
    )

    db.add(new_study_group)
    db.commit()
    db.refresh(new_study_group)

    return new_study_group


@study_group_router.get("/", response_model=List[StudyGroupResponse])
async def list_study_groups(
    db: Session = Depends(get_db)
):
    return db.query(StudyGroup).all()


@study_group_router.get(
    "/{study_group_id}",
    response_model=StudyGroupResponse
)
async def detail_study_group(
    study_group_id: int,
    db: Session = Depends(get_db)
):
    study_group_db = db.query(StudyGroup).filter(
        StudyGroup.id == study_group_id
    ).first()

    if not study_group_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай группа жок"
        )

    return study_group_db


@study_group_router.put(
    "/{study_group_id}",
    response_model=StudyGroupResponse
)
async def update_study_group(
    study_group_id: int,
    study_group: StudyGroupUpdate,
    db: Session = Depends(get_db)
):
    study_group_db = db.query(StudyGroup).filter(
        StudyGroup.id == study_group_id
    ).first()

    if not study_group_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай группа жок"
        )

    if study_group.course_id is not None:
        course_db = db.query(Course).filter(
            Course.id == study_group.course_id
        ).first()

        if not course_db:
            raise HTTPException(
                status_code=404,
                detail="Мындай курс жок"
            )

    if study_group.teacher_id is not None:
        teacher_db = db.query(UserProfile).filter(
            UserProfile.id == study_group.teacher_id
        ).first()

        if not teacher_db:
            raise HTTPException(
                status_code=404,
                detail="Мындай мугалим жок"
            )

    update_data = study_group.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(study_group_db, field, value)

    db.commit()
    db.refresh(study_group_db)

    return study_group_db


@study_group_router.delete(
    "/{study_group_id}",
    response_model=dict
)
async def delete_study_group(
    study_group_id: int,
    db: Session = Depends(get_db)
):
    study_group_db = db.query(StudyGroup).filter(
        StudyGroup.id == study_group_id
    ).first()

    if not study_group_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай группа жок"
        )

    db.delete(study_group_db)
    db.commit()

    return {
        "message": "Группа өчүрүлдү"
    }