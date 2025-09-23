import requests

r = requests.get("https://reqres.in/api/users?page=2")
print(r.status_code, r.json())

r = requests.get("https://reqres.in/api/users/2")
print(r.status_code, r.json())

r = requests.get("https://reqres.in/api/users/23")
print(r.status_code, r.json())

r = requests.get("https://reqres.in/api/unknown")
print(r.status_code, r.json())

r = requests.get("https://reqres.in/api/unknown/2")
print(r.status_code, r.json())

r = requests.get("https://reqres.in/api/unknown/23")
print(r.status_code, r.json())

r = requests.post("https://reqres.in/api/users", json={"name": "morpheus", "job": "leader"})
print(r.status_code, r.json())

r = requests.put("https://reqres.in/api/users/2", json={"name": "morpheus", "job": "zion resident"})
print(r.status_code, r.json())

r = requests.patch("https://reqres.in/api/users/2", json={"job": "zion resident"})
print(r.status_code, r.json())

r = requests.delete("https://reqres.in/api/users/2")
print(r.status_code, {})

r = requests.post("https://reqres.in/api/register", json={"email": "eve.holt@reqres.in", "password": "pistol"})
print(r.status_code, r.json())

r = requests.post("https://reqres.in/api/register", json={"email": "sydney@fife"})
print(r.status_code, r.json())

r = requests.post("https://reqres.in/api/login", json={"email": "eve.holt@reqres.in", "password": "cityslicka"})
print(r.status_code, r.json())

r = requests.post("https://reqres.in/api/login", json={"email": "peter@klaven"})
print(r.status_code, r.json())

r = requests.get("https://reqres.in/api/users?delay=3")
print(r.status_code, r.json())

