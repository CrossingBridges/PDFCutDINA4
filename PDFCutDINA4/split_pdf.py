from pdf2image import convert_from_path
from PIL import Image
import math
from fpdf import FPDF
import os

Image.MAX_IMAGE_PIXELS = None  # Entfernt die Begrenzung

def is_white(image):
    # Überprüfen, ob das Bild komplett weiß ist
    width, height = image.size
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if r != 255 or g != 255 or b != 255:
                return False
    return True

def split_pdf_into_a4(path, scale_factor):
    # Konvertieren Sie das PDF in ein Bild
    images = convert_from_path(path)

    # Für jedes Bild (jede Seite im PDF)
    for i, image in enumerate(images):
        # Skaliert das Bild auf den gegebenen Skalierungsfaktor der Originalgröße
        width, height = image.size
        image = image.resize((int(width * scale_factor), int(height * scale_factor)))

        # Die Größe des Bildes in Pixel
        width, height = image.size

        # Die Größe eines A4-Papiers in Pixel bei 300 dpi
        a4_width = 2480
        a4_height = 3508

        # Anzahl der aufgeteilten Bilder
        cols = math.ceil(width / a4_width)
        rows = math.ceil(height / a4_height)

        # Teilen Sie das Bild auf
        for row in range(rows):
            for col in range(cols):
                left = col * a4_width
                top = row * a4_height
                right = min((col + 1) * a4_width, width)  # Begrenzen Sie das Rechte auf das Bildende
                bottom = min((row + 1) * a4_height, height)  # Begrenzen Sie das Untere auf das Bildende

                # Schneiden Sie das Bild aus und fügen Sie einen weißen Hintergrund hinzu, falls benötigt
                cropped = Image.new("RGB", (a4_width, a4_height), "white")
                cropped_part = image.crop((left, top, right, bottom))
                cropped.paste(cropped_part, (0, 0, right - left, bottom - top))

                # Überprüfen, ob das Bild komplett weiß ist, und überspringen Sie es
                if is_white(cropped_part):
                    continue

                # Speichern Sie das ausgeschnittene Bild als PDF
                pdf = FPDF(unit="pt", format=[a4_width, a4_height])
                pdf.add_page()

                # Konvertieren Sie das Bild in ein temporäres JPEG-Bild, um es mit fpdf zu verwenden
                cropped.save("temp.jpg", "JPEG")

                # Fügen Sie das Bild zur PDF-Seite hinzu
                pdf.image("temp.jpg", 0, 0)

                # Speichern Sie die PDF-Seite
                pdf_name = f"{os.path.splitext(path)[0]}_page_{i}_part_{row}_{col}.pdf"
                pdf.output(pdf_name, "F")

# Fragt den Benutzer nach dem Namen und dem Pfad der Datei
file_name = input("Bitte geben Sie den Namen der PDF-Datei ein (ohne .pdf): ")
file_path = input("Bitte geben Sie den Pfad zur Datei an, falls sie sich nicht im gleichen Verzeichnis befindet. Andernfalls drücken Sie einfach Enter: ")
pdf_path = os.path.join(file_path, file_name + ".pdf")

# Fragt den Benutzer nach dem Skalierungsfaktor
scale_factor = input("Bitte geben Sie den Skalierungsfaktor ein (z.B. 0.36 für 36%): ")
scale_factor = float(scale_factor)

# Teilen Sie die PDF-Datei
split_pdf_into_a4(pdf_path, scale_factor)
