import os
import subprocess
import datetime
import shutil
import sys
import re

# === Einstellungen ===
REPO_PATH = "/home/student/AI_Influencer" 
SOURCE_BASE_PATH = "/home/student/Fooocus-API/outputs/files"

# === Aktuelles Datum (Ordnername) ===
today = datetime.date.today().isoformat()
source_folder = os.path.join(SOURCE_BASE_PATH, today)

if not os.path.isdir(source_folder):
    print(f"Kein Ausgabeordner für heute gefunden unter: {source_folder}")
    sys.exit(1)

# === Zielordner im Repo
target_folder = os.path.join(REPO_PATH, "images_to_post")
os.makedirs(target_folder, exist_ok=True)

# === Bilder kopieren und Endung -<Zahl> entfernen
for file_name in os.listdir(source_folder):
    if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        full_src_path = os.path.join(source_folder, file_name)

        # Endung -<Zahl> vor der Dateiendung entfernen (z. B. 040-0.png → 040.png)
        name, ext = os.path.splitext(file_name)
        cleaned_name = re.sub(r"-\d+$", "", name)
        new_file_name = cleaned_name + ext

        full_dst_path = os.path.join(target_folder, new_file_name)
        shutil.copy2(full_src_path, full_dst_path)
        print(f"Kopiert und umbenannt: {file_name} → {new_file_name}")

# === Git-Befehle ===
try:
    relative_path = os.path.join("generated_images", today)
    subprocess.run(["git", "add", relative_path], cwd=REPO_PATH, check=True)
    subprocess.run(["git", "commit", "-m", f"Auto: Add images from {today}"], cwd=REPO_PATH, check=True)
    subprocess.run(["git", "push"], cwd=REPO_PATH, check=True)
    print("Änderungen erfolgreich an GitHub gepusht.")
except subprocess.CalledProcessError as e:
    print(f"Fehler bei Git-Befehl: {e}")
    sys.exit(1)
