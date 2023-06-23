from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf, output_pdf):
    pdf = PdfReader(input_pdf)
    total_pages = len(pdf.pages)

    output = PdfWriter()

    for page_number in range(total_pages):
        page = pdf.pages[page_number]
        output.add_page(page)

        if (page_number + 1) % 4 == 0:  # Anzahl der Seiten pro DIN A4-Seite
            output_filename = output_pdf.format((page_number + 1) // 4)
            with open(output_filename, "wb") as output_file:
                output.write(output_file)
            output = PdfWriter()

    if len(output.pages) != 0:
        output_filename = output_pdf.format((total_pages // 4) + 1)
        with open(output_filename, "wb") as output_file:
            output.write(output_file)

# Beispielaufruf
input_pdf = "PV1.pdf"
output_pdf = "seiten_{}.pdf"  # Hier kannst du den Namen und das Format der Ausgabedateien anpassen

split_pdf(input_pdf, output_pdf)
