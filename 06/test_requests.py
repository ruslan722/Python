import requests
import time

BASE_URL = "http://127.0.0.1:8000"
r = requests.get(f"{BASE_URL}/survey/")
print("GET /survey/ ->", r.status_code, r.json(), "\n")
time.sleep(1)

# --- POST /survey/ ---
survey_data = {
    "user_id": 10,
    "question": "Как ваше настроение сегодня?",
    "score": 9
}
r = requests.post(f"{BASE_URL}/survey/", json=survey_data)
print("POST /survey/ ->", r.status_code, r.json(), "\n")
survey_id = r.json().get("survey_id")
time.sleep(1)

# --- PUT /survey/{id} ---
update_data = {"score": 5}
r = requests.put(f"{BASE_URL}/survey/{survey_id}", json=update_data)
print(f"PUT /survey/{survey_id} ->", r.status_code, r.json(), "\n")
time.sleep(1)

# --- DELETE /survey/{id} ---
r = requests.delete(f"{BASE_URL}/survey/{survey_id}")
print(f"DELETE /survey/{survey_id} ->", r.status_code, r.json(), "\n")
time.sleep(1)

# --- GET /quotes/ ---
r = requests.get(f"{BASE_URL}/quotes/")
print("GET /quotes/ ->", r.status_code, r.json(), "\n")
time.sleep(1)

# --- POST /quotes/ ---
quote_data = {
    "text": "Сегодня — лучший день, чтобы начать что-то новое!",
    "mood_tag": "happy"
}
r = requests.post(f"{BASE_URL}/quotes/", json=quote_data)
print("POST /quotes/ ->", r.status_code, r.json(), "\n")
quote_id = r.json().get("quote_id")
time.sleep(1)


update_quote = {"text": "Каждый день — шанс стать лучше!"}
r = requests.put(f"{BASE_URL}/quotes/{quote_id}", json=update_quote)
print(f"PUT /quotes/{quote_id} ->", r.status_code, r.json(), "\n")
time.sleep(1)


r = requests.delete(f"{BASE_URL}/quotes/{quote_id}")
print(f"DELETE /quotes/{quote_id} ->", r.status_code, r.json(), "\n")
time.sleep(1)

# --- GET /state/{user_id} ---
r = requests.get(f"{BASE_URL}/state/3")
print("GET /state/1 ->", r.status_code, r.json(), "\n")
time.sleep(1)

# --- GET /motivation/{user_id} ---
r = requests.get(f"{BASE_URL}/motivation/3")
print("GET /motivation/1 ->", r.status_code, r.json(), "\n")

