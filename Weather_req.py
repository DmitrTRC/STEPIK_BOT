import requests as req

url1 = 'http://wttr.in/?M2F&lang=ru'
url2 = 'http://wttr.in/moon?F&lang=ru'
response = req.get(url1)
print(response.text)
response = req.get(url2)
print(response.text)
