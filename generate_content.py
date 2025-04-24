import os
import random
import openai
import requests
import base64
from openai import OpenAI

# Liste von Zitaten mit Stimmung
quotes = [
    ("Manchmal ist ein Ende auch ein neuer Anfang.", "sad"),
    ("Jeder Tag ist eine neue Chance.", "happy"),
    ("Auch der längste Weg beginnt mit dem ersten Schritt.", "neutral"),
    ("Glück ist das Einzige, das sich verdoppelt, wenn man es teilt.", "joyful"),
    ("In der Stille findest du dich selbst.", "calm")
]

def generate_prompt(text, mood):
    return f"A {mood} background with the quote: '{text}' written beautifully in the image. Soft lighting, cinematic, elegant, Instagram style."

def generate_image_with_openai(prompt):
    # OpenAI-Client initialisieren
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Bild generieren
    result = client.images.generate(
        model="gpt-image-1",  # Beispielmodell, ggf. anpassen je nach dem, was verfügbar ist
        prompt=prompt
    )
    
    # Bild in Base64 dekodieren
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    
    # Bild speichern
    with open("bild.jpg", "wb") as f:
        f.write(image_bytes)

def main():
    # Zufälliges Zitat und Stimmung auswählen
    quote, mood = random.choice(quotes)
    
    # Prompt generieren
    prompt = generate_prompt(quote, mood)
    
    # Bild generieren
    generate_image_with_openai(prompt)
    
    # Zitat in einer Textdatei speichern
    with open("caption.txt", "w", encoding="utf-8") as f:
        f.write(quote)

if __name__ == "__main__":
    main()
