from PyPDF2 import PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas





def split_pdf(input_pdf, output_pdf):
    pdf = PdfReader(input_pdf)
    total_pages = len(pdf.pages)

    c = canvas.Canvas("temp.pdf", pagesize=landscape(A4))

    for page_number in range(total_pages):
        page = pdf.pages[page_number]
        c.setPageSize(page.cropbox.lower_left + page.cropbox.upper_right)
        c.showPage()

        if (page_number + 1) % 4 == 0:  # Anzahl der Seiten pro DIN A4-Seite
            c.save()
            output_filename = output_pdf.format((page_number + 1) // 4)
            writer = PdfWriter()
            writer.add_page(crop_to_fit(page))  # Hier wird die aktuelle Seite übergeben
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)
            c = canvas.Canvas("temp.pdf", pagesize=landscape(A4))

    c.save()
    if total_pages % 4 != 0:
        output_filename = output_pdf.format((total_pages // 4) + 1)
        writer = PdfWriter()
        writer.add_page(crop_to_fit(pdf.pages[-1]))  # Hier wird die letzte Seite übergeben
        with open(output_filename, "wb") as output_file:
            writer.write(output_file)



def crop_to_fit(page):
    width = page.mediabox.width
    height = page.mediabox.height

    new_height = width * 0.7
    crop_top = (height - new_height) / 2
    crop_bottom = height - crop_top

    new_page = page.crop(0, crop_bottom, width, crop_top)
    new_page.trimBox.lowerLeft = (0, crop_bottom)
    new_page.trimBox.upperRight = (width, crop_top)
    new_page.cropBox.lowerLeft = (0, crop_bottom)
    new_page.cropBox.upperRight = (width, crop_top)

    return new_page



# Beispielaufruf
input_pdf = "PV1.pdf"
output_pdf = "seiten_{}.pdf"  # Hier kannst du den Namen und das Format der Ausgabedateien anpassen

split_pdf(input_pdf, output_pdf)
