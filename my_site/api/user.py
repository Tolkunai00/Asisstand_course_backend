from my_site.db.models import UserProfile
from my_site.db.schema import UserCreate, UserUpdate, UserResponse
from my_site.db.database import SessionLocal

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List


user_router = APIRouter(
    prefix="/users",
    tags=["User CRUD"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@user_router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    user_db = db.query(UserProfile).filter(
        UserProfile.email == user.email
    ).first()

    if user_db:
        raise HTTPException(
            status_code=400,
            detail="Мындай email менен колдонуучу бар"
        )

    new_user = UserProfile(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@user_router.get("/", response_model=List[UserResponse])
async def list_users(
    db: Session = Depends(get_db)
):
    return db.query(UserProfile).all()


@user_router.get("/{user_id}", response_model=UserResponse)
async def detail_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_db = db.query(UserProfile).filter(
        UserProfile.id == user_id
    ).first()

    if not user_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай колдонуучу жок"
        )

    return user_db


@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    user_db = db.query(UserProfile).filter(
        UserProfile.id == user_id
    ).first()

    if not user_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай колдонуучу жок"
        )

    update_data = user.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(user_db, field, value)

    db.commit()
    db.refresh(user_db)

    return user_db


@user_router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_db = db.query(UserProfile).filter(
        UserProfile.id == user_id
    ).first()

    if not user_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай колдонуучу жок"
        )

    db.delete(user_db)
    db.commit()

    return {
        "message": "Колдонуучу өчүрүлдү"
    }