import requests
import json
import os

API_URL = "http://127.0.0.1:8888/v1/generation/image-prompt"
IMAGE_PATH = "images/image.png" 
PROMPT = "A wise, modern virtual mentor with a calm, friendly expression, sitting in a minimalistic futuristic room filled with soft ambient lighting and bookshelves, wearing elegant casual clothes, glowing eyes symbolizing deep knowledge, soft color tones, cinematic lighting, ultra-realistic portrait, serene atmosphere"

# Bild einlesen
if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"Bild nicht gefunden: {IMAGE_PATH}")

with open(IMAGE_PATH, "rb") as f:
    face_image = f.read()

# Request-Parameter definieren
params = {
    "prompt": PROMPT,
    "image_prompts": [ 
        {
            "cn_type": "FaceSwap"
        }
    ]
}

# API-Call senden
print("Sende Anfrage an Fooocus-API (FaceSwap)...")

response = requests.post(
    url=API_URL,
    data=params,
    files={
        "cn_img1": ("image.png", face_image, "image/png")
    }
)

# Antwort verarbeiten
try:
    response.raise_for_status()
    result = response.json()
    print("Antwort empfangen:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except requests.exceptions.HTTPError as e:
    print("HTTP Fehler:", e)
    print(response.text)
except Exception as e:
    print("Allgemeiner Fehler:", e)
