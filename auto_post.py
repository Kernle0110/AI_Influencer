import os
from instagrapi import Client

username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(username, password)

with open("caption.txt", "r", encoding="utf-8") as f:
    caption = f.read()

cl.photo_upload("bild.jpg", caption)
print("✅ Bild gepostet mit Caption.")
