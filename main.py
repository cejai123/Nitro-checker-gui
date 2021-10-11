from tkinter import *
import random
import string
import requests
import threading
from threading import Thread
import time

class nitrochecker(Tk):
    def __init__(self):
        super().__init__()
        self.good = 0
        self.bad = 0
        self.bad_text = Label(text="Bad: 0");self.bad_text.pack()
        self.good_text = Label(text="Good: 0");self.good_text.pack()
        self.mybutton = Button(text="Start", command=lambda:threading.Thread(target=self.checker1, daemon=True).start()).pack()
    def checker(self):
        with open("proxies.txt") as file:
            self.proxies = file.read().splitlines()
        self.codes="".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase,k=16))
        while True:
            self.proxy = random.choice(self.proxies)
            try:
                coderequest = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{self.codes}?country_code=ES&payment_source_id=868308987400032296&with_application=false&with_subscription_plan=true",
                proxies={"https": f"socks4://{self.proxy}"})
                if coderequest.status_code == 200:
                    with open("good.txt","a") as file:
                        file.write(f"https://discord.gift/{self.codes}\n")
                    self.good+=1
                    return
                elif coderequest.status_code == 404:
                    with open("bad.txt","a") as file:
                        file.write(f"https://discord.gift/{self.codes}\n")
                    self.bad+=1
                    return
            except:
                pass
    def updater(self):
        while 1:
            try:
                self.good_text["text"] = "Good:",self.good
                self.bad_text["text"] = "Bad:",self.bad 
            except:
                pass
            finally:
                time.sleep(0.1)               
    def checker1(self):
        Thread(target=self.updater, daemon=True).start()
        while 1:
            if threading.active_count() < 500 + 2:
                threading.Thread(target=self.checker,daemon=True).start()
            else:
                time.sleep(0.5)
if __name__ == "__main__":
    g = nitrochecker()
    g.geometry("400x150")
    g.title("Nitro Checker 2.0")
    g.mainloop()