import os
import random
import openai
import requests

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
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Neue API-Aufrufmethode verwenden
    response = openai.images.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    # URL des generierten Bildes
    image_url = response['data'][0]['url']
    
    # Bild herunterladen und speichern
    img_data = requests.get(image_url).content
    with open("bild.jpg", "wb") as f:
        f.write(img_data)

def main():
    quote, mood = random.choice(quotes)  # Zufälliges Zitat und Stimmung auswählen
    prompt = generate_prompt(quote, mood)  # Prompt generieren
    generate_image_with_openai(prompt)  # Bild mit OpenAI generieren
    
    # Zitat in einer Textdatei speichern
    with open("caption.txt", "w", encoding="utf-8") as f:
        f.write(quote)

if __name__ == "__main__":
    main()
