import subprocess
import time
import socket
import sys

def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host, port)) == 0

try:
    # === 1. Starte Ollama-Server ===
    print("🔍 Prüfe, ob Ollama-Server läuft...")
    if not is_port_open("localhost", 11434):
        print("🟡 Starte Ollama-Server...")
        subprocess.Popen(['start', 'cmd', '/k', 'ollama serve'], shell=True)
        time.sleep(5)
        if not is_port_open("localhost", 11434):
            raise RuntimeError("❌ Ollama-Server konnte nicht gestartet werden.")
    print("🟢 Ollama-Server aktiv.")

    # === 2. Starte Modell (Mistral) ===
    print("🟡 Starte Mistral-Modell in neuem Terminal...")
    subprocess.Popen(['start', 'cmd', '/k', 'ollama run llama3'], shell=True)
    time.sleep(10)  # Wartezeit für Initialisierung

    # === 3. Generiere Zitat ===
    print("✍️  Führe generate_content.py aus...")
    for i in range(20):
        result = subprocess.run(['python', 'generate_content.py'], check=True)
    print("✅ Zitat erfolgreich generiert.")

except subprocess.CalledProcessError as e:
    print(f"❌ Fehler bei Ausführung eines Skripts: {e}")
    sys.exit(1)

except Exception as e:
    print(f"❌ Allgemeiner Fehler: {e}")
    sys.exit(1)
