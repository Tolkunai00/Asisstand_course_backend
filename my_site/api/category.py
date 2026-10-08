from my_site.db.models import Category
from my_site.db.schema import CategoryCreate, CategoryUpdate, CategoryResponse
from my_site.db.database import SessionLocal

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List


category_router = APIRouter(
    prefix="/categories",
    tags=["Category CRUD"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@category_router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    category_db = db.query(Category).filter(
        Category.category_name == category.category_name
    ).first()

    if category_db:
        raise HTTPException(
            status_code=400,
            detail="Мындай категория бар"
        )

    new_category = Category(
        category_name=category.category_name
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@category_router.get("/", response_model=List[CategoryResponse])
async def list_categories(
    db: Session = Depends(get_db)
):
    return db.query(Category).all()


@category_router.get("/{category_id}", response_model=CategoryResponse)
async def detail_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category_db = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай категория жок"
        )

    return category_db


@category_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    category_db = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай категория жок"
        )

    update_data = category.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(category_db, field, value)

    db.commit()
    db.refresh(category_db)

    return category_db


@category_router.delete("/{category_id}", response_model=dict)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category_db = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category_db:
        raise HTTPException(
            status_code=404,
            detail="Мындай категория жок"
        )

    db.delete(category_db)
    db.commit()

    return {
        "message": "Категория өчүрүлдү"
    }