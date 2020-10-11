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
    if len(sys.argv) < 3:
        raise IOError(f"Arguments Error - not enough arguments:\n{sys.argv[0]} [PDF file 1] [PDF file 2] ... (At least 2 PDF files, more are optional)")

    pdf_files_list_to_merge = sys.argv[1:]

    for f in pdf_files_list_to_merge:
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
print("Merging...")

merger = PyPDF2.PdfFileMerger
for pdf_file in pdf_files_list_to_merge:
    merger.append(pdf_file)

new_merged_pdf_file = f"Merged_PDF_{datetime.datetime.now}.pdf"
merger.write(new_merged_pdf_file)

print("PDF Merged successfully")