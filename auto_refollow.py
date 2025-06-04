import os

from instagrapi import Client
import time

# === Login ===
username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(username, password)

# === Follower holen ===
my_user_id = cl.user_id_from_username(username)
followers = cl.user_followers(my_user_id)
print(f"👥 Follower: {len(followers)}")

# === Followings holen ===
followings = cl.user_following(my_user_id)
print(f"➡️  Bereits gefolgt: {len(followings)}")

# === Berechnung: Noch nicht zurückgefolgt
followers_ids = set(followers.keys())
followings_ids = set(followings.keys())

not_followed_back = followers_ids - followings_ids
print(f"🔍 Noch nicht zurückgefolgt: {len(not_followed_back)} User")

# === Automatisch folgen (max 5 pro Run)
MAX_FOLLOWS = 5
counter = 0

for user_id in not_followed_back:
    # 👉 Username direkt aus followers dict holen → KEINE public request nötig!
    username_to_follow = followers[user_id].username
    print(f"➕ Folge jetzt: {username_to_follow}")

    cl.user_follow(user_id)
    counter += 1
    time.sleep(5)  # Delay für Sicherheit

    if counter >= MAX_FOLLOWS:
        print(f"✅ Max {MAX_FOLLOWS} Follows erreicht. Stoppe.")
        break

print("🏁 Fertig.")

