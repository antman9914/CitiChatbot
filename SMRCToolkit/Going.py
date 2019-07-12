import requests


try:
    #res = requests.get("https://www.baidu.com/ping").ok
    res = requests.get("http://localhost:9000/ping").ok
    print(res)
except:
    print("error raised")
