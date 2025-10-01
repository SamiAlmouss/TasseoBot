import requests
import threading
import time
url0 = "https://tasseobot.onrender.com/"
url1="÷https://quiz-flask1-ping.onrender.com"
def req():
    while True:
        try:
            r = requests.get(url0, timeout=100)
            r = requests.get(url1, timeout=100)
            time.sleep(900)
        except requests.RequestException as e:
            print("Request failed:", e)

t = threading.Thread(target=req)
t.start()
