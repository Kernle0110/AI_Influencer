import subprocess
import sys


try:
    # === 1. Poste Bild ===
    print("📤 Führe auto_post.py aus...")
    subprocess.run(['python', 'auto_post.py'], check=True)
    print("✅ Bild erfolgreich gepostet.")

    # === 2. Refollow  ===
    print("📤 Führe auto_refollow.py aus...")
    # subprocess.run(['python', 'auto_refollow.py'], check=True)
    print("✅ Follower erfolgreich gefolt.")

    # === 3. Answer comment  ===
    print("📤 Führe answer_comments.py aus...")
    subprocess.run(['python', 'answer_comments.py'], check=True)
    print("✅ Kommentare erfolgreich beantwortet.")

    print("🏁 Workflow abgeschlossen.")

except subprocess.CalledProcessError as e:
    print(f"❌ Fehler bei Ausführung eines Skripts: {e}")
    sys.exit(1)

except Exception as e:
    print(f"❌ Allgemeiner Fehler: {e}")
    sys.exit(1)
