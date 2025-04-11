import requests
import json

url = "http://localhost:8000/accounts/api/token/verify/"

response = requests.post(url, data={"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NDEyMTI5LCJpYXQiOjE3NDQzNjg5MjksImp0aSI6IjU4MWUxMmM3NjNhNzQwYTFhNWIxNTFlYzEwYjc0NTg1IiwidXNlcl9pZCI6MTAsInVzZXJuYW1lIjoibmV3X3VzZXIxIn0.3Oa04WK7_74wULR5tvkkTv8UoZYFn-omWeEkEurzWCk"})

print(response.text, response.status_code)




