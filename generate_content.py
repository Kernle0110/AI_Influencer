import requests
import json

# === Prompt-Definition ===
prompt_text = (
    "Erzeuge exakt EIN tiefgründiges deutsches Lebenszitat zum Thema ‚Lebensweisheiten‘. "
    "Das Zitat muss ein sinnvoller, grammatikalisch korrekter Satz in deutscher Sprache sein "
    "und mindestens 5 Wörter enthalten. "
    "Das Zitat soll philosophisch oder emotional klingen, aber eindeutig verständlich bleiben. "
    "Nach dem Zitat folgt eine neue Zeile mit 1 bis 3 Schlagwörtern, die das Zitat beschreiben. "
    "Gib nur diesen einen Satz und die Schlagwörter zurück – keine weiteren Erklärungen, keine Autorenangabe. "
    "Vermeide erfundene Namen, Formulierungen aus anderen Sprachen oder unsinnige Satzstrukturen. "
    "Antwortformat:\n<Zitat>\n<Stichwort1, Stichwort2, Stichwort3>"
)

payload = {
    "model": "llama3",
    "prompt": prompt_text,
    "options": {"temperature": 1.0}
}
# 2. Neue Anfrage zur Umformulierung
payload = {
    "model": "llama3",
    "prompt": (
        f"Formuliere folgendes Zitat stilistisch schöner und klarer, aber behalte die Bedeutung:\n"
        f"{prompt_text}"
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

# === 1. Nur das aktuellste Zitat speichern ===
with open("caption.txt", "w", encoding="utf-8") as f:
    f.write(full_response)

# === 2. Zitat an History-Datei anhängen ===
with open("captions_history.txt", "a", encoding="utf-8") as f:
    f.write(full_response + "\n\n")
