import requests
import random

# Access Token and User-ID
ACCESS_TOKEN = "EAAJAIdThZAZCgBOxOQQXuUA1VbzPqvHmMClK52JKQEFt1oL8xihHJfnG2FQZBgUEBGCr9rRsD9rgiCMDUWvqXRO2Hf5TuHoFvrjb8FV3ghqLXupudUOTPbDGaKZBtwoRbpZAu91se0XaiGVbx9E9inV0Y3ExZAJcJwgf3kvW2rhConOvjTMS8T3ZAKefPbvpMJQUpS6JwzGbzThGy2Y29KTKUzezE9KtP0o"
IG_USER_ID = "17841473970080369"

# Mögliche Antworten
ANTWORTEN = [
    "Danke dir! 🙌",
    "Mega lieb von dir! ❤️",
    "Danke für deinen Kommentar! ✨",
    "🔥🔥🔥",
    "Danke für dein Feedback! 💬",
    "🙏 Danke für deinen Support!",
    "Freut mich, dass du vorbeischaust! 👀",
    "❤️",
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

def get_replies(comment_id):
    url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"
    params = {
        "fields": "id,from",
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    return response.json().get('data', [])

def has_replied(comment_id):
    replies = get_replies(comment_id)
    for reply in replies:
        user = reply.get('from', {})
        if user.get('id') == IG_USER_ID:
            return True
    return False

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
#        print(f"📸 Beitrag: {media.get('id')} – {media.get('caption')}")
        comments = get_comments(media['id'])
        for comment in comments:
            comment_id = comment['id']
            if not has_replied(comment_id):
                reply_to_comment(comment_id)
            else:
                print(f"⏩ Kommentar {comment_id} wurde schon von dir beantwortet – übersprungen.")


if __name__ == "__main__":
    main()
