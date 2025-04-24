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
    response = openai.Image.create(
        prompt=prompt,
        model="dall-e-3",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    img_data = requests.get(image_url).content
    with open("bild.jpg", "wb") as f:
        f.write(img_data)

def main():
    quote, mood = random.choice(quotes)
    prompt = generate_prompt(quote, mood)
    generate_image_with_openai(prompt)
    with open("caption.txt", "w", encoding="utf-8") as f:
        f.write(quote)

if __name__ == "__main__":
    main()
