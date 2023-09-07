import requests

url = 'http://localhost:8080/invocations'
headers = {
    'Content-Type': 'application/json'
}
data = 'Translate to German: How are you?'

response = requests.post(url, headers=headers, data=data)
print(response.text)
