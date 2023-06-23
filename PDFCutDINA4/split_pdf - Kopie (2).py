from pdf2image import convert_from_path
from PIL import Image
import math
from fpdf import FPDF
import os

Image.MAX_IMAGE_PIXELS = None  # Entfernt die Begrenzung

def is_white(pixel):
    r, g, b = pixel
    return r == 255 and g == 255 and b == 255

def should_skip_page(image):
    width, height = image.size
    border_offset_mm = 5
    border_offset_pixels = int((border_offset_mm / 25.4) * 300)  # convert mm to pixels

    # Überprüfen, ob der Rest des Bildes außerhalb des 5-mm-Offsets weiß ist
    for x in range(border_offset_pixels, width):
        for y in range(border_offset_pixels, height):
            pixel = image.getpixel((x, y))
            if not is_white(pixel):
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

                # Überprüfen, ob das Bild übersprungen werden sollte, und überspringen Sie es
                if should_skip_page(cropped_part):
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
scale_percent = input("Bitte geben Sie den Skalierungsfaktor in Prozent ein (z.B. 36 für 36%): ")
scale_factor = float("0." + scale_percent)

# Teilen Sie die PDF-Datei
split_pdf_into_a4(pdf_path, scale_factor)
