import requests
import random

# Access Token and User-ID
ACCESS_TOKEN = os.getenv("IG_TOKEN_ELIAS")
IG_USER_ID = os.getenv("IG_USERID_ELIAS")

# Mögliche Antworten
ANTWORTEN = [
    "Danke dir! 🙌",
    "Mega lieb von dir! ❤️",
    "Danke für deinen Kommentar! ✨",
    "🔥🔥🔥",
    "Danke für dein Feedback! 💬",
    "🙏 Danke für deinen Support!"
    "Freut mich, dass du vorbeischaust! 👀"
    "❤️"
    "💯"
]

# Antwort zufällig wählen
def zufällige_antwort():
    return random.choice(ANTWORTEN)

# Eigene Medien holen
def get_user_media():
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    params = {
        "fields": "id,caption",
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    return response.json().get('data', [])

# Kommentare eines Beitrags holen
def get_comments(media_id):
    url = f"https://graph.facebook.com/v19.0/{media_id}/comments"
    params = {
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    return response.json().get('data', [])

# Kommentar automatisch beantworten
def reply_to_comment(comment_id):
    message = zufällige_antwort()
    url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"
    params = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        print(f"💬 Kommentar {comment_id} geantwortet mit: {message}")
    else:
        print(f"❌ Fehler bei Kommentar {comment_id}: {response.text}")

def main():
    media_list = get_user_media()
    for media in media_list:
        print(f"📸 Beitrag: {media.get('id')} – {media.get('caption')}")
        comments = get_comments(media['id'])
        for comment in comments:
            reply_to_comment(comment['id'])

if __name__ == "__main__":
    main()
