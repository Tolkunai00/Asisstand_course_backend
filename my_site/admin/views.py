from sqladmin import ModelView
from my_site.db.models import (UserProfile, Category, Course, StudyGroup, Application, Enrollment)


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [
        UserProfile.id, UserProfile.full_name,
        UserProfile.email, UserProfile.role,
        UserProfile.is_active,UserProfile.created_at
    ]

    name = "User"
    name_plural = "Users"

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class CategoryAdmin(ModelView, model=Category):
    column_list = [
        Category.id,
        Category.category_name
    ]

    name = "Category"
    name_plural = "Categories"

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class CourseAdmin(ModelView, model=Course):
    column_list = [
        Course.id,
        Course.course_name,
        Course.category_id,
        Course.level,
        Course.price,
        Course.duration_weeks,
        Course.is_active,
        Course.status
    ]

    name = "Course"
    name_plural = "Courses"

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class StudyGroupAdmin(ModelView, model=StudyGroup):
    column_list = [
        StudyGroup.id,
        StudyGroup.name,
        StudyGroup.course_id,
        StudyGroup.teacher_id,
        StudyGroup.starts_on,
        StudyGroup.ends_on,
        StudyGroup.status_recruiting
    ]

    name = "Study Group"
    name_plural = "Study Groups"

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class ApplicationAdmin(ModelView, model=Application):
    column_list = [
        Application.id,
        Application.student_id,
        Application.course_id,
        Application.manager_id,
        Application.comment,
        Application.status_application,
        Application.created_at
    ]

    name = "Application"
    name_plural = "Applications"

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class EnrollmentAdmin(ModelView, model=Enrollment):
    column_list = [
        Enrollment.id,
        Enrollment.student_id,
        Enrollment.group_id,
        Enrollment.status_enrollment,
        Enrollment.created_at
    ]

    name = "Enrollment"
    name_plural = "Enrollments"

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True