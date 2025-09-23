from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connect import Course

app = FastAPI()


class CourseSchema(BaseModel):
    title: str
    instructor: str
    duration: int
    level: str



@app.get("/api/course")
def get_courses():
    return list(Course.select())



@app.get("/api/course/{course_id}")
def get_course(course_id: int):
    course = Course.get_or_none(Course.id == course_id)
    if course:
        return course
    raise HTTPException(status_code=404, detail="Курс не найден")



@app.post("/api/course")
def create_course(course: CourseSchema):   
    new_course = Course.create(
        title=course.title,
        instructor=course.instructor,
        duration=course.duration,
        level=course.level
    )
    return new_course



@app.put("/api/course/{course_id}")
def update_course(course_id: int, updated: CourseSchema):
    course = Course.get_or_none(Course.id == course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    course.title = updated.title
    course.instructor = updated.instructor
    course.duration = updated.duration
    course.level = updated.level
    course.save()
    return course



@app.delete("/api/course/{course_id}")
def delete_course(course_id: int):
    course = Course.get_or_none(Course.id == course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    course.delete_instance()
    return {"message": "Удалено"}
