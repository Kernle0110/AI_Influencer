import os
import subprocess
import datetime
import shutil
import sys

# === Einstellungen ===
REPO_PATH = "/home/student/your-github-repo"  # Pfad zum lokalen Klon deines GitHub-Repos
SOURCE_BASE_PATH = "/home/student/Fooocus_API/outputs/files"

# === Aktuelles Datum (Ordnername) ===
today = datetime.date.today().isoformat()
source_folder = os.path.join(SOURCE_BASE_PATH, today)

if not os.path.isdir(source_folder):
    print(f"Kein Ausgabeordner für heute gefunden unter: {source_folder}")
    sys.exit(1)

# === Zielordner im Repo (z.B. unter 'generated_images/yyyy-mm-dd') ===
target_folder = os.path.join(REPO_PATH, "generated_images", today)
os.makedirs(target_folder, exist_ok=True)

# === Bilder kopieren ===
for file_name in os.listdir(source_folder):
    if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        full_src_path = os.path.join(source_folder, file_name)
        full_dst_path = os.path.join(target_folder, file_name)
        shutil.copy2(full_src_path, full_dst_path)
        print(f"Kopiert: {file_name}")

# === Git-Befehle ===
try:
    subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True)
    subprocess.run(["git", "commit", "-m", f"Add images from {today}"], cwd=REPO_PATH, check=True)
    subprocess.run(["git", "push"], cwd=REPO_PATH, check=True)
    print("Änderungen erfolgreich an GitHub gepusht.")
except subprocess.CalledProcessError as e:
    print(f"Fehler bei Git-Befehl: {e}")
    sys.exit(1)
