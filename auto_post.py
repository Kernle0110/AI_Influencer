import csv
import os
import shutil

from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont

# === Login ===
username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(username, password)

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
caption_text = f"{quote}\n\n{hashtags}"

# === Hochladen ===
cl.photo_upload("bild_caption.jpg", caption_text)
print("✅ Bild mit transparentem Text-Hintergrund gepostet.")

# === Move image to archive folder ===
if not os.path.exists(archive_folder):
    os.makedirs(archive_folder)

target_path = os.path.join(archive_folder, image_file)
shutil.move(image_path, target_path)
print(f"📂 Moved image {image_file} to {archive_folder}.")

