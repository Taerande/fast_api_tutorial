from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel
import requests

app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: str
    

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/cities")
def get_cities():
    results = []

    for city in db:
        request_url = f"https://worldtimeapi.org/api/timezone/{city['timezone']}"
        r = requests.get(request_url)
        current_time = r.json()['datetime']
        results.append({"name": city['name'], "timezone": city['timezone'], "current_time": current_time})

    return results

@app.get("/cities/{city_id}")
def get_city(city_id: int):
    city = db[city_id-1]
    request_url = f"https://worldtimeapi.org/api/timezone/{city['timezone']}"
    r = requests.get(request_url)
    current_time = r.json()['datetime']
    return {"name": city['name'], "timezone": city['timezone'], "current_time": current_time}

@app.post("/cities")
def create_city(city: City):
    db.append(city.dict())
    return db[-1]

@app.delete("/cities/{city_id}")
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}


students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 12"
    },
    2: {
        "name": "Jane",
        "age": 16,
        "class": "year 11"
    }
}


@app.get('/get-student/{student_id}')
def get_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0, lt=3)):
    return {"student_id": student_id}

@app.get('/get-by-name/{student_id}')
def get_student(*, student_id: int, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}

class Student(BaseModel):
    name: str
    age: int
    class_: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_: Optional[str] = None


@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id] = student
    return students[student_id]


@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):

    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.class_ != None:
        students[student_id].class_ = student.class_

    return students[student_id]


@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}