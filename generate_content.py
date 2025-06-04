import csv
import os

import requests
import json

# === Prompt-Definition ===
prompt_text = (
    "Erzeuge exakt EIN tiefgründiges deutsches Lebenszitat zum Thema ‚Lebensweisheiten‘. "
    "Das Zitat muss ein sinnvoller, grammatikalisch korrekter Satz in deutscher Sprache sein "
    "und mindestens 5 Wörter enthalten. "
    "Das Zitat soll philosophisch oder emotional klingen, aber eindeutig verständlich bleiben. "
    "Nach dem Zitat folgt GENAU EINE neue Zeile mit GENAU 1 bis 3 einzelnen STICHWÖRTERN, getrennt durch Kommata. "
    "Gib KEINE zusätzlichen Erklärungen, KEINE Autorenangabe, KEINE Anführungszeichen. "
    "Gib NUR das reine Ergebnis in diesem Format zurück:"
    "Zitat\nStichwort1, Stichwort2, Stichwort3"
)

payload = {
    "model": "llama3",
    "prompt": prompt_text,
    "options": {"temperature": 1.0}
}

# === Anfrage senden ===
res = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)
full_response = ""

for chunk in res.iter_lines():
    if chunk:
        data = json.loads(chunk)
        full_response += data.get("response", "")

full_response = full_response.strip()

# 2. Neue Anfrage zur Umformulierung
payload = {
    "model": "llama3",
    "prompt": (
        f"Formuliere folgendes Zitat mit Stichwörtern stilistisch schöner und klarer, aber behalte die Bedeutung:\n"
        f"{full_response}\n"
        f"Antworte EXAKT in folgendem Format, ohne zusätzliche Wörter, ohne Anführungszeichen, ohne Zwischenüberschriften:\n"
        f"Zitat\nStichwort1, Stichwort2, Stichwort3"

    ),
    "options": {"temperature": 0.7}
}

# === Anfrage senden ===
res = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)
full_response = ""

for chunk in res.iter_lines():
    if chunk:
        data = json.loads(chunk)
        full_response += data.get("response", "")

full_response = full_response.strip()

# 3. Neue Anfrage zur Umformulierung
payload = {
    "model": "llama3",
    "prompt": (
        f"{full_response}\n"
        f"Bringe den folgenden Text, bestehend aus Zitat und Stichwörtern, EXAKT in folgendes Format, ohne zusätzliche Wörter, ohne Anführungszeichen, ohne zusätzliche Leerzeilen:\n"
        f"Zitat\nStichwort1, Stichwort2, Stichwort3"

    ),
    "options": {"temperature": 0.7}
}

# === Anfrage senden ===
res = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)
full_response = ""

for chunk in res.iter_lines():
    if chunk:
        data = json.loads(chunk)
        full_response += data.get("response", "")

full_response = full_response.strip()

# === Zitat & Schlagworte trennen ===
parts = full_response.split("\n")
zitat = parts[0].strip()
schlagworte = ""
if len(parts) > 1:
    schlagworte = parts[1].replace("-", "").strip()

# === CSV-Datei vorbereiten ===
csv_file = "zitate.csv"

# Wenn CSV noch nicht existiert → Kopfzeile schreiben
if not os.path.exists(csv_file):
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nr", "zitat", "schlagworte"])

# === Nächste Nummer bestimmen ===
next_nr = 1
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # Kopfzeile überspringen
    for row in reader:
        if row and row[0].isdigit():
            nr = int(row[0])
            if nr >= next_nr:
                next_nr = nr + 1

# Nummer formatieren mit führenden Nullen
nr_str = f"{next_nr:03}"

# === In CSV anhängen ===
with open(csv_file, "a", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([nr_str, zitat, schlagworte])

print(f"✅ Neues Zitat gespeichert als {nr_str}: {zitat}")