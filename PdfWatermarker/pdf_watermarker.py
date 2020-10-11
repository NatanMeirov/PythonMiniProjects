# Imports
import sys
import os
import datetime
try:
    import PyPDF2
except ImportError:
    print("Please make sure to install PyPDF2 library first: use 'pip install PyPDF2' command")
    sys.exit()


# Validations
try:
    if len(sys.argv) > 3:
        raise IOError(f"Arguments Error - too much arguments:\n{sys.argv[0]} [PDF file to watermark] [PDF file to use as watermark]")
    if len(sys.argv) < 3:
        raise IOError(f"Arguments Error - not enough arguments:\n{sys.argv[0]} [PDF file to watermark] [PDF file to use as watermark]")

    pdf_to_watermark = sys.argv[1]
    pdf_watermarker = sys.argv[2]

    for f in [pdf_to_watermark, pdf_watermarker]:
        if not os.path.exists(f):
            raise FileNotFoundError(f"File Not Found Error: {f} file Does not exists")
        if not os.path.isfile(f):
            raise FileNotFoundError(f"File Not Found Error: {f} exists, but it is not a file")
        if str(os.path.basename(f)).split(".")[1] != "pdf":
            raise FileNotFoundError(f"File Not Found Error: {f} exists and it is a file, but it is not a PDF file")

except IOError as e:
    print(e)
    sys.exit()
except FileNotFoundError as e:
    print(e)
    sys.exit()


# Processing
print("Watermarking...")

template = PyPDF2.PdfFileReader(open(pdf_to_watermark, "rb"))
watermark = PyPDF2.PdfFileReader(open(pdf_watermarker, "rb"))

output_file_name = f"Watermarked_{str(os.path.basename(pdf_to_watermark)).split('.')[0]}_{datetime.datetime.now}.pdf"
output_file = PyPDF2.PdfFileWriter()

for i in range(template.getNumPages()):
    current_page = template.getPage(i)
    current_page.mergePage(watermark.getPage(0)) # Watermarking using the first page of the Watermark PDF file

    output_file.addPage(current_page)

with open(output_file_name, "wb") as f:
    output_file.write(f)

print("Watermarking has completed successfully")