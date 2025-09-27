import requests
BASE_URL = "http://127.0.0.1:8000/api/course"

def get_courses():
    r = requests.get(BASE_URL)
    print("GET /course")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

def get_course():
    r = requests.get(BASE_URL + "/1")
    print("GET /course/1")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

def create_course():
    r = requests.post(BASE_URL)
    print("POST /course")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

def update_course():
    r = requests.put(BASE_URL + "/1")
    print("PUT /course/1")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

def delete_course():
    r = requests.delete(BASE_URL + "/1")
    print("DELETE /course/1")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

get_courses()
get_course()
create_course()
update_course()
delete_course()
