import requests
import base64
import os
import csv
import re

# === Einstellungen ===
FACE_IMAGE = "base_image_elias.png"
FACE_IMAGE_PATH = "/home/student/AI_Influencer/fooocus_image_generation_scripts/" + FACE_IMAGE
CSV_PATH = "/home/student/AI_Influencer/zitate.csv"
OUTPUT_DIR = "/home/student/AI_Influencer/images_to_post"
API_URL = "http://127.0.0.1:8888/v2/generation/image-prompt"

BASE_PROMPT = "a cinematic portrait of a thoughtful man, realistic lighting, soft shadows, shallow depth of field"
ALLOWED_IMAGES = ["base_image_elias.png", "base_image_maya.png"]

# === Bild-Pfad prüfen ===
if FACE_IMAGE not in ALLOWED_IMAGES or not os.path.isfile(FACE_IMAGE_PATH):
    print(f"Fehler: Ungültiger oder nicht vorhandener Bildpfad: {FACE_IMAGE_PATH}")
    exit(1)

# === Nächste Bildnummer finden ===
existing_files = [f for f in os.listdir(OUTPUT_DIR) if re.match(r"\d{3}\.png", f)]
if existing_files:
    last_number = max([int(f.split(".")[0]) for f in existing_files])
    next_number = f"{last_number + 1:03}"
else:
    next_number = "001"

next_filename = f"{next_number}.png"
print(f"Nächstes Bild: {next_filename}")

# === CSV lesen ===
with open(CSV_PATH, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    row = None
    for r in reader:
        if r['nr'] == next_number:
            row = r
            break

if not row:
    print(f"Keine Zeile mit Nummer {next_number} in {CSV_PATH} gefunden.")
    exit(1)

# === Prompt bauen ===
full_prompt = f"{BASE_PROMPT}, {row['schlagworte']}"
print(f"Verwendeter Prompt:\n{full_prompt}")

# === Bild als Base64 laden ===
with open(FACE_IMAGE_PATH, "rb") as f:
    face_b64 = base64.b64encode(f.read()).decode("utf-8")

# === Payload ===
payload = {
    "prompt": full_prompt,
    "negative_prompt": "",
    "style_selections": ["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp", "Fooocus Photograph"],
    "performance_selection": "Quality",
    "aspect_ratios_selection": "1152*896",
    "image_number": 1,
    "image_seed": -1,
    "sharpness": 2,
    "guidance_scale": 4,
    "base_model_name": "juggernautXL_v8Rundiffusion.safetensors",
    "refiner_model_name": "None",
    "refiner_switch": 0.5,
    "loras": [
        {"enabled": True, "model_name": "sd_xl_offset_example-lora_1.0.safetensors", "weight": 0.1},
        *[{"enabled": True, "model_name": "None", "weight": 1} for _ in range(4)]
    ],
    "advanced_params": {
        "adaptive_cfg": 7,
        "adm_scaler_end": 0.3,
        "adm_scaler_negative": 0.8,
        "adm_scaler_positive": 1.5,
        "black_out_nsfw": False,
        "clip_skip": 2,
        "freeu_enabled": False,
        "inpaint_engine": "v2.6",
        "inpaint_strength": 1,
        "refiner_swap_method": "joint",
        "sampler_name": "dpmpp_2m_sde_gpu",
        "scheduler_name": "karras",
        "vae_name": "Default (model)"
    },
    "save_meta": True,
    "meta_scheme": "fooocus",
    "save_extension": "png",
    "save_name": next_number,
    "require_base64": True,
    "async_process": False,
    "image_prompts": [
        {
            "cn_img": face_b64,
            "cn_stop": 1.0,
            "cn_weight": 1.0,
            "cn_type": "FaceSwap"
        }
    ]
}

# === Anfrage senden ===
print("Sende Anfrage an Fooocus-API...")

try:
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        print(f"Bilder wurden erfolgreich erstellt als {next_filename}!")
        print("Schau im Ordner: Fooocus-API/outputs/files/<heutiges Datum>")
    else:
        print(f"Fehler bei der Anfrage. Statuscode: {response.status_code}")
        print(f"Nachricht: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Verbindungsfehler: {e}")
