import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap, QColor
from PyQt5.QtCore import Qt
import os
from dotenv import load_dotenv

load_dotenv()  # lädt automatisch die .env-Datei

class ZitatApp(QWidget):
    def __init__(self):
        super().__init__()
        #self.background_path = "Neon_Social_Icons.png"
        self.background_path = "Social_Media_Influence.png"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Zitat & Hashtag Eingabe")
        self.setStyleSheet("color: white; font-family: 'Segoe UI';")

        # Hauptlayout (zentriert die Glass-Karte)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignCenter)

        # === GLAS-CARD ===
        self.glass_card = QWidget()
        self.glass_card.setFixedSize(1000, 600)
        self.glass_card.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.2);  /* leicht getönt */
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
            }
        """)
        self.glass_card.setGraphicsEffect(self.get_shadow())

        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)

        # === Titel ===
        title = QLabel("Zitat & Hashtags")
        title.setFont(QFont("Segoe UI Semibold", 30))
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)

        # === Zitatfeld ===
        self.zitat_feld = QTextEdit()
        self.zitat_feld.setFont(QFont("Segoe UI", 18))
        self.zitat_feld.setPlaceholderText("Zitat hier eingeben...")
        self.zitat_feld.setFocusPolicy(Qt.StrongFocus)  # Fokus erlaubt
        self.zitat_feld.setStyleSheet(self.glass_input_style())
        content_layout.addWidget(self.zitat_feld)

        # === Hashtagfeld ===
        self.hashtag_feld = QLineEdit()
        self.hashtag_feld.setFont(QFont("Segoe UI", 18))
        self.hashtag_feld.setPlaceholderText("#hashtag1 #hashtag2")
        self.hashtag_feld.setFocusPolicy(Qt.StrongFocus)
        self.hashtag_feld.setStyleSheet(self.glass_input_style())
        content_layout.addWidget(self.hashtag_feld)

        # === Button ===
        submit_btn = QPushButton("Posten")
        submit_btn.setFont(QFont("Segoe UI", 20))
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 120, 215, 0.6);
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 215, 0.85);
            }
        """)
        submit_btn.clicked.connect(self.submit_data)
        content_layout.addWidget(submit_btn)

        self.glass_card.setLayout(content_layout)
        main_layout.addWidget(self.glass_card)

        self.update_background()

        # === Cursor direkt aktiv bei Start ===
        self.zitat_feld.setFocus()

    def get_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        return shadow

    def glass_input_style(self):
        return """
            QTextEdit, QLineEdit {
                background-color: rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 10px;
                color: white;
            }
            QTextEdit:focus, QLineEdit:focus {
                border: 1px solid white;
                background-color: rgba(255, 255, 255, 0.08);
            }
        """

    def update_background(self):
        pixmap = QPixmap(self.background_path)
        if pixmap.isNull():
            print("⚠️ Hintergrundbild konnte nicht geladen werden.")
            return

        # Skaliere Hintergrundbild auf Fenstergröße
        scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # Konvertiere zu OpenCV-Bild
        image = scaled_pixmap.toImage().convertToFormat(QImage.Format_RGB888)
        ptr = image.bits()
        ptr.setsize(image.width() * image.height() * 3)
        cv_image = np.array(ptr).reshape(image.height(), image.width(), 3)

        # === Simulierter Blur-Bereich ===
        x = int((self.width() - self.glass_card.width()) / 2)
        y = int((self.height() - self.glass_card.height()) / 2)
        w = self.glass_card.width()
        h = self.glass_card.height()

        blur_area = cv_image[y:y + h, x:x + w]
        blurred = cv2.GaussianBlur(blur_area, (35, 35), 0)
        cv_image[y:y + h, x:x + w] = blurred

        # Zurück in QPixmap
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        qimg = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        final_pixmap = QPixmap.fromImage(qimg)

        # Als Hintergrund setzen
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(final_pixmap))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.update_background()
        return super().resizeEvent(event)

    def submit_data(self):
        zitat = self.zitat_feld.toPlainText()
        hashtags = self.hashtag_feld.text().replace(",", " ")
        print("Zitat:", zitat)
        print("Hashtags:", hashtags)
        self.post(zitat, hashtags)
        self.zitat_feld.clear()
        self.hashtag_feld.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def post(self, zitat, hashtags):
        import csv
        import os
        import shutil
        import subprocess
        import time

        import requests
        from PIL import Image, ImageDraw, ImageFont

        ACCESS_TOKEN = os.getenv("IG_ELIAS_PAGE_TOKEN")
        INSTAGRAM_USER_ID = os.getenv("IG_ELIAS_USER_ID")

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
        quote = zitat

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

        # === Git Commit & Push (damit RAW-URL das neue Bild lädt) ===
        try:
            subprocess.run(["git", "config", "user.name", "Juliaxrbl"], check=True)
            subprocess.run(["git", "config", "user.email", "juliariebel02@gmail.com"], check=True)
            subprocess.run(["git", "add", "bild_caption.jpg"], check=True)
            subprocess.run(["git", "commit", "-m", f"Update caption image for post {post_number}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("✅ Bild erfolgreich committet und gepusht.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Git-Fehler beim Commit oder Push: {e}")
            exit(1)

        # === Instagram-Caption erzeugen ===
        hashtags = ' '.join(hashtags.split())

        # === Add manual hashtags
        manual_hashtags = ("#poesie "
                           "#zitat "
                           "#zitate "
                           "#sprüche "
                           "#erfolg "
                           "#lebensweisheiten "
                           "#glücklich "
                           "#erfolgreich "
                           "#mindset "
                           "#weisheiten "
                           "#positivdenken "
                           "#veränderung "
                           "#gedanken"
                           )

        # === Combine all hashtags
        hashtags = f"{hashtags} {manual_hashtags.strip()}"
        caption_text = f"{quote}\n\n{hashtags}"

        # === RAW-URL zur Bilddatei erzeugen (für die Instagram Graph API)
        RAW_IMAGE_URL = f"https://raw.githubusercontent.com/Kernle0110/AI_Influencer/main/bild_caption.jpg"
        print(f"📷 Lade Bild via: {RAW_IMAGE_URL}")

        # === 1. Container erstellen
        create_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_USER_ID}/media"
        create_params = {
            "image_url": RAW_IMAGE_URL,
            "caption": caption_text,
            "access_token": ACCESS_TOKEN
        }

        # === Hochladen ===
        create_res = requests.post(create_url, data=create_params)
        create_json = create_res.json()
        print("📦 Container-Response:", create_json)

        if "id" not in create_json:
            print("❌ Fehler beim Erstellen des Containers")
            exit(1)

        container_id = create_json["id"]

        # === 2. Warten + Veröffentlichen
        time.sleep(2)
        publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_USER_ID}/media_publish"
        publish_params = {
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN
        }
        publish_res = requests.post(publish_url, data=publish_params)
        publish_json = publish_res.json()
        print("🚀 Veröffentlichung-Response:", publish_json)

        if "id" in publish_json:
            print("✅ Testpost erfolgreich veröffentlicht! Post-ID:", publish_json["id"])
        else:
            print("❌ Fehler beim Veröffentlichen:", publish_json)
            exit(1)
        print("✅ Bild mit transparentem Text-Hintergrund gepostet.")

        # === Move image to archive folder ===
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)

        target_path = os.path.join(archive_folder, image_file)
        shutil.move(image_path, target_path)
        print(f"📂 Moved image {image_file} to {archive_folder}.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    fenster = ZitatApp()
    fenster.showFullScreen()
    sys.exit(app.exec_())