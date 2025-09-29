import requests
import threading
import time
url0 = "https://tasseobot.onrender.com/"
def req():
    while True:
        try:
            r = requests.get(url0, timeout=100)
            time.sleep(300)
        except requests.RequestException as e:
            print("Request failed:", e)

t = threading.Thread(target=req)
t.start()
