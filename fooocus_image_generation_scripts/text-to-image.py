import requests

API_URL = "http://127.0.0.1:8888/v1/generation/text-to-image"

PROMPT = "A wise, modern virtual mentor with a calm, friendly expression, sitting in a minimalistic futuristic room filled with soft ambient lighting and bookshelves, wearing elegant casual clothes, glowing eyes symbolizing deep knowledge, soft color tones, cinematic lighting, ultra-realistic portrait, serene atmosphere"

payload = {
    "prompt": PROMPT,
    "negative_prompt": "",
    "style_selections": ["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp", "Fooocus Photograph"],
    "performance_selection": "Quality",
    "aspect_ratios_selection": "1152*896",
    "image_number": 2,
    "image_seed": -1,
    "sharpness": 2,
    "guidance_scale": 4,
    "base_model_name": "juggernautXL_v8Rundiffusion.safetensors",
    "refiner_model_name": "None",
    "refiner_switch": 0.5,
    "loras": [
        {"enabled": True, "model_name": "sd_xl_offset_example-lora_1.0.safetensors", "weight": 0.1},
        *[
            {"enabled": True, "model_name": "None", "weight": 1}
            for _ in range(4)
        ]
    ],
    "advanced_params": {
        "adaptive_cfg": 7,
        "adm_scaler_end": 0.3,
        "adm_scaler_negative": 0.8,
        "adm_scaler_positive": 1.5,
        "black_out_nsfw": False,
        "canny_high_threshold": 128,
        "canny_low_threshold": 64,
        "clip_skip": 2,
        "controlnet_softness": 0.25,
        "debugging_cn_preprocessor": False,
        "debugging_dino": False,
        "debugging_enhance_masks_checkbox": False,
        "debugging_inpaint_preprocessor": False,
        "dino_erode_or_dilate": 0,
        "disable_intermediate_results": False,
        "disable_preview": False,
        "disable_seed_increment": False,
        "freeu_b1": 1.01,
        "freeu_b2": 1.02,
        "freeu_enabled": False,
        "freeu_s1": 0.99,
        "freeu_s2": 0.95,
        "inpaint_advanced_masking_checkbox": True,
        "inpaint_disable_initial_latent": False,
        "inpaint_engine": "v2.6",
        "inpaint_erode_or_dilate": 0,
        "inpaint_respective_field": 1,
        "inpaint_strength": 1,
        "invert_mask_checkbox": False,
        "mixing_image_prompt_and_inpaint": False,
        "mixing_image_prompt_and_vary_upscale": False,
        "overwrite_height": -1,
        "overwrite_step": -1,
        "overwrite_switch": -1,
        "overwrite_upscale_strength": -1,
        "overwrite_vary_strength": -1,
        "overwrite_width": -1,
        "refiner_swap_method": "joint",
        "sampler_name": "dpmpp_2m_sde_gpu",
        "scheduler_name": "karras",
        "skipping_cn_preprocessor": False,
        "vae_name": "Default (model)"
    },
    "save_meta": True,
    "meta_scheme": "fooocus",
    "save_extension": "png",
    "save_name": "",
    "read_wildcards_in_order": False,
    "require_base64": True,
    "async_process": False,
    "webhook_url": ""
}

print("Sende Anfrage an Fooocus-API...")

try:
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        print("Bilder wurden erfolgreich erstellt!")
        print("Die Bilder befinden sichs im Ordner: Fooocus-API\\outputs\\files\\<heutiges Datum>")
    else:
        print(f"Fehler bei der Anfrage. Statuscode: {response.status_code}, Nachricht: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Verbindungsfehler: {e}")
