from fastapi import FastAPI
import uvicorn
from my_site.api import (user, category, course, study, application, enrollment)


app = FastAPI(title="Course Management")
app.include_router(user.user_router)
app.include_router(category.category_router)
app.include_router(course.course_router)
app.include_router(study.study_group_router)
app.include_router(application.application_router)
app.include_router(enrollment.enrollment_router)


@app.get("/")
async def root():
    return {"message": "API is working"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)