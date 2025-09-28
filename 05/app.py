import requests
BASE_URL = "http://127.0.0.1:8000/api/course"

def get_courses():
    r = requests.get(BASE_URL)
    print("GET /course")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

def get_course():
    r = requests.get(BASE_URL + "/3")
    print("GET /course/3")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

def create_course():
    a = {
        "title": "Курс Python",
        "instructor": "Иван Иванов",
        "duration": 30,
        "level": "Начальный"
    }
    r = requests.post(BASE_URL, json=a)
    print("POST /course")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")



def update_course():
    a = {
        "title": "Обновленный курс Python",
        "instructor": "Иван Иванов",
        "duration": 45,
        "level": "Средний"
    }
    r = requests.put(BASE_URL + "/2", json=a)
    print("PUT /course/2")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

def delete_course():
    r = requests.delete(BASE_URL + "/6")
    print("DELETE /course/6")
    print("Статус:", r.status_code)
    print("Ответ:", r.json(), "\n")

get_courses()
get_course()
create_course()
update_course()
delete_course()
