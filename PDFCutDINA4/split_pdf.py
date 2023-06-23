from pdf2image import convert_from_path
from PIL import Image
import math
from fpdf import FPDF

Image.MAX_IMAGE_PIXELS = None  # Entfernt die Begrenzung

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
                cropped.paste(image.crop((left, top, right, bottom)), (0, 0, right - left, bottom - top))

                # Speichern Sie das ausgeschnittene Bild als PDF
                pdf = FPDF(unit="pt", format=[a4_width, a4_height])
                pdf.add_page()

                # Konvertieren Sie das Bild in ein temporäres JPEG-Bild, um es mit fpdf zu verwenden
                cropped.save("temp.jpg", "JPEG")

                # Fügen Sie das Bild zur PDF-Seite hinzu
                pdf.image("temp.jpg", 0, 0)

                # Speichern Sie die PDF-Seite
                pdf_name = f"{path.split('.')[0]}_page_{i}_part_{row}_{col}.pdf"
                pdf.output(pdf_name, "F")


# Pfad zur PDF-Datei
pdf_path = 'PV1.pdf'

# Frage den Benutzer nach dem Skalierungsfaktor
scale_factor = input("Bitte geben Sie den Skalierungsfaktor ein (z.B. 0.36 für 36%): ")
scale_factor = float(scale_factor)

# Teilen Sie die PDF-Datei
split_pdf_into_a4(pdf_path, scale_factor)

