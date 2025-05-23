import requests
import json
import os

# === Konfiguration ===
API_URL = "http://127.0.0.1:8888/v1/generation/image-inpaint-outpaint"
IMAGE_PATH = "images/image.png"      
MASK_PATH = "images/m.png"         
PROMPT = "a glowing symbol of wisdom painted over the masked area"

# === Dateien einlesen ===
if not os.path.exists(IMAGE_PATH) or not os.path.exists(MASK_PATH):
    raise FileNotFoundError("Bild oder Maske nicht gefunden!")

with open(IMAGE_PATH, "rb") as f:
    image = f.read()

with open(MASK_PATH, "rb") as f:
    mask = f.read()

# === Parameter ===
params = {
    "inpaint_additional_prompt": PROMPT,
    "async_process": True
}

# === API-Call ===
response = requests.post(
    url=API_URL,
    data=params,
    files={
        "input_image": image,
        "input_mask": mask
    }
)

# === Ergebnis ausgeben ===
try:
    response.raise_for_status()
    result = response.json()
    print("✅ Inpaint-Ergebnis:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print("❌ Fehler beim Inpainting:", e)
