from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from my_site.db.models import UserRoleChoices, LevelCourse, Status, StudyStatus, ApplicationStatus, EnrollmentStatus

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: UserRoleChoices

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRoleChoices] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: UserRoleChoices
    is_active: bool
    created_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)



class CategoryCreate(BaseModel):
    category_name: str

class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    category_name: str
    model_config = ConfigDict(from_attributes=True)



class CourseCreate(BaseModel):
    course_name: str
    category_id: int
    descriptions: str
    level: LevelCourse = LevelCourse.beginner
    price: int
    duration_weeks: int
    is_active: bool
    status: Status

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    category_id: Optional[int] = None
    descriptions: Optional[str] = None
    level: Optional[LevelCourse] = None
    price: Optional[int] = None
    duration_weeks: Optional[int] = None
    is_active: Optional[bool] = None
    status: Optional[Status] = None

class CourseResponse(BaseModel):
    id: int
    course_name: str
    category_id: int
    descriptions: str
    level: LevelCourse
    price: int
    duration_weeks: int
    is_active: bool
    status: Status
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)



class StudyGroupCreate(BaseModel):
    name: str
    course_id: int
    teacher_id: int
    starts_on: datetime
    ends_on: datetime
    status_recruiting: StudyStatus

class StudyGroupUpdate(BaseModel):
    name: Optional[str] = None
    course_id: Optional[int] = None
    teacher_id: Optional[int] = None
    starts_on: Optional[datetime] = None
    ends_on: Optional[datetime] = None
    status_recruiting: Optional[StudyStatus] = None

class StudyGroupResponse(BaseModel):
    id: int
    name: str
    course_id: int
    teacher_id: int
    starts_on: datetime
    ends_on: datetime
    status_recruiting: StudyStatus
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)



class ApplicationCreate(BaseModel):
    student_id: int
    course_id: int
    manager_id: int
    comment: Optional[str] = None
    status_application: ApplicationStatus

class ApplicationUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    manager_id: Optional[int] = None
    comment: Optional[str] = None
    status_application: Optional[ApplicationStatus] = None

class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    manager_id: int
    comment: Optional[str]
    status_application: ApplicationStatus
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)



class EnrollmentCreate(BaseModel):
    student_id: int
    group_id: int
    status_enrollment: EnrollmentStatus

class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = None
    group_id: Optional[int] = None
    status_enrollment: Optional[EnrollmentStatus] = None

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    group_id: int
    status_enrollment: EnrollmentStatus
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)