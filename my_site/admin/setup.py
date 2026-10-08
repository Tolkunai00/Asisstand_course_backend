from fastapi import FastAPI
from sqladmin import Admin
from my_site.db.database import engine
from my_site.admin.views import (UserProfileAdmin, CategoryAdmin, CourseAdmin,StudyGroupAdmin, ApplicationAdmin, EnrollmentAdmin)


def setup_admin(app: FastAPI):
    admin = Admin(app=app, engine=engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(CourseAdmin)
    admin.add_view(StudyGroupAdmin)
    admin.add_view(ApplicationAdmin)
    admin.add_view(EnrollmentAdmin)