import requests

r = requests.get("https://mexc.com")
print(r.status_code)
