from my_site.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, ForeignKey, DateTime, Boolean, Text
from enum import Enum as PyEnum
from typing import List, Optional
from datetime import datetime


class UserRoleChoices(str, PyEnum):
    teacher = 'teacher'
    manager = 'manager'
    admin = 'admin'

class LevelCourse(str, PyEnum):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'

class Status(str, PyEnum):
    free = 'free'
    plus = 'plus'

class StudyStatus(str, PyEnum):
    recruiting = 'recruiting'
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'

class ApplicationStatus(str, PyEnum):
    new = 'new'
    in_progress = 'in_progress'
    accepted = 'accepted'
    rejected = 'rejected'
    cancelled = 'cancelled'

class EnrollmentStatus(str, PyEnum):
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'


class UserProfile(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String)
    role: Mapped[UserRoleChoices] = mapped_column(Enum(UserRoleChoices))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String)

    course: Mapped[List['Course']] = relationship(back_populates='course_category', cascade='all, delete-orphan')


class Course(Base):
    __tablename__ = 'course'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    descriptions: Mapped[str] = mapped_column(Text)
    level: Mapped[LevelCourse] = mapped_column(Enum(LevelCourse), default=LevelCourse.beginner)
    price: Mapped[int] = mapped_column(Integer)
    duration_weeks: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean)
    status: Mapped[Status] = mapped_column(Enum(Status))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    course_category: Mapped['Category'] = relationship(Category, back_populates='course', cascade='all, delete-orphan')


class StudyGroup(Base):
    __tablename__ = 'study'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    course_id: Mapped[int] = mapped_column(Integer)
    teacher_id: Mapped[int] = mapped_column(Integer)
    starts_on: Mapped[datetime] = mapped_column(DateTime)
    ends_on: Mapped[datetime] = mapped_column(DateTime)
    status_recruiting: Mapped[StudyStatus] = mapped_column(Enum(StudyStatus))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Application(Base):
    __tablename__ = 'application'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer)
    course_id: Mapped[int] = mapped_column(Integer)
    manager_id: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(String)
    status_application: Mapped[ApplicationStatus] = mapped_column(Enum(ApplicationStatus))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    update_at: Mapped[datetime] = mapped_column(DateTime)


class Enrollment(Base):
    __tablename__ = 'enrollment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)
    status_enrollment: Mapped[EnrollmentStatus] = mapped_column(Enum(EnrollmentStatus))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    update_at: Mapped[datetime] = mapped_column(DateTime)



