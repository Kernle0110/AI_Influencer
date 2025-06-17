import csv
import os
import shutil
import time

import requests
from PIL import Image, ImageDraw, ImageFont


ACCESS_TOKEN = os.getenv("IG_TOKEN_ELIAS")
INSTAGRAM_USER_ID = os.getenv("IG_USERID_ELIAS")

# === Folders ===
images_folder = "images_to_post"
archive_folder = "archive_images"

# === Find first image in folder ===
image_files = sorted([f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.png'))])

if not image_files:
    print("❌ No image found in images folder.")
    exit(1)

image_file = image_files[0]  # Take first image
image_path = os.path.join(images_folder, image_file)

# === Extract number from filename (without .jpg/.png)
post_number = os.path.splitext(image_file)[0]

# === Load quote and keywords from zitate.csv ===
quote_text = ""
keywords_text = ""

with open("zitate.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["nr"] == post_number:
            quote_text = row["zitat"].strip()
            keywords_text = row["schlagworte"].strip()
            break

if not quote_text:
    print(f"❌ No quote found for number {post_number}")
    exit(1)

quote = quote_text
keywords = [kw.strip() for kw in keywords_text.split(",") if kw.strip()]

# === Print quote into picture ===
image = Image.open(image_path).convert("RGBA")
width, height = image.size

# === Schriftart laden ===
font_path = "PlayfairDisplay.ttf"
font_size = 40
try:
    font = ImageFont.truetype(font_path, font_size)
except:
    font = ImageFont.load_default()

# === Funktion: Text umbrechen ===
def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# === Text vorbereiten ===
draw_temp = ImageDraw.Draw(image)
max_text_width = int(width * 0.65)  # Weniger Wörter pro Zeile
lines = wrap_text(quote, font, max_text_width, draw_temp)
line_spacing = 40
line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
total_text_height = len(lines) * (line_height + line_spacing)
y_start = (height - total_text_height) / 2

# === Transparentes Overlay vorbereiten ===
overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
overlay_draw = ImageDraw.Draw(overlay)

# === Text & Hintergrund zeichnen ===
padding = 40
y = y_start

for line in lines:
    bbox = overlay_draw.textbbox((0, 0), line, font=font)
    line_width = bbox[2] - bbox[0]
    line_height = bbox[3] - bbox[1]
    x = (width - line_width) / 2

    # Halbtransparente schwarze Box
    overlay_draw.rectangle(
        [(x - padding, y - padding), (x + line_width + padding, y + line_height + padding)],
        fill=(0, 0, 0, 128)  # 50 % transparent
    )

    y += line_height + line_spacing

# === Bild und Overlay zusammenführen ===
image = Image.alpha_composite(image, overlay)
draw_final = ImageDraw.Draw(image)

# === Text erneut zeichnen (über der Box) ===
y = y_start
for line in lines:
    bbox = draw_final.textbbox((0, 0), line, font=font)
    line_width = bbox[2] - bbox[0]
    x = (width - line_width) / 2
    draw_final.text((x, y), line, font=font, fill="white")
    y += line_height + line_spacing

# === In RGB konvertieren & speichern ===
image = image.convert("RGB")
image.save("bild_caption.jpg")

# === Instagram-Caption erzeugen ===
hashtags = " ".join(f"#{k.replace(' ', '')}" for k in keywords)

# === Add manual hashtags
manual_hashtags = ("#poesie "
                   "#zitat "
                   "#zitate "
                   "#sprüche "
                   "#erfolg "
                   "#lebensweisheiten "
                   "#glücklich "
                   "#erfolgreich "
                   "#mindset "
                   "#weisheiten "
                   "#positivdenken "
                   "#veränderung "
                   "#gedanken"
                   )

# === Combine all hashtags
hashtags = f"{hashtags} {manual_hashtags.strip()}"
caption_text = f"{quote}\n\n{hashtags}"

# === RAW-URL zur Bilddatei erzeugen (für die Instagram Graph API)
RAW_IMAGE_URL = f"https://raw.githubusercontent.com/Kernle0110/AI_Influencer/main/bild_caption.jpg"
print(f"📷 Lade Bild via: {RAW_IMAGE_URL}")

# === 1. Container erstellen
create_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_USER_ID}/media"
create_params = {
    "image_url": RAW_IMAGE_URL,
    "caption": caption_text,
    "access_token": ACCESS_TOKEN
}

# === Hochladen ===
create_res = requests.post(create_url, data=create_params)
create_json = create_res.json()
print("📦 Container-Response:", create_json)

if "id" not in create_json:
    print("❌ Fehler beim Erstellen des Containers")
    exit(1)

container_id = create_json["id"]

# === 2. Warten + Veröffentlichen
time.sleep(2)
publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_USER_ID}/media_publish"
publish_params = {
    "creation_id": container_id,
    "access_token": ACCESS_TOKEN
}
publish_res = requests.post(publish_url, data=publish_params)
publish_json = publish_res.json()
print("🚀 Veröffentlichung-Response:", publish_json)

if "id" in publish_json:
    print("✅ Testpost erfolgreich veröffentlicht! Post-ID:", publish_json["id"])
else:
    print("❌ Fehler beim Veröffentlichen:", publish_json)
print("✅ Bild mit transparentem Text-Hintergrund gepostet.")

# === Move image to archive folder ===
if not os.path.exists(archive_folder):
    os.makedirs(archive_folder)

target_path = os.path.join(archive_folder, image_file)
shutil.move(image_path, target_path)
print(f"📂 Moved image {image_file} to {archive_folder}.")

