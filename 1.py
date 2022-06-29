import requests
r = requests.get("http://0.0.0.0:8080/")
print(r.headers['Server'])