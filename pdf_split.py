# split a pdf by pages

from PyPDF2 import PdfFileReader, PdfFileWriter
import os

def split_pdf(pdf_to_split, split_size=20):
    """Split a pdf into chunks.
    """

    docname = os.path.basename(os.path.splitext(pdf_to_split)[0])
    docdir = os.path.dirname(os.path.abspath(pdf_to_split))

    os.makedirs(os.path.join(docdir,docname))

    my_pdf=PdfFileReader(stream=pdf_to_split)

    docpart = 0
    docparts = my_pdf.getNumPages() / split_size
    while docpart < docparts:
        output=PdfFileWriter()
        for i in range(split_size):
            if docpart*split_size + i < my_pdf.getNumPages():
                output.addPage(my_pdf.getPage(docpart*split_size + i))
        with open(os.path.join(docdir,docname,docname+'-part-%03d.pdf' % docpart), 'wb') as outputStream:
            output.write(outputStream)
        docpart += 1

split_pdf('/home/mason/topics/historyofswedish01stra.pdf', 1)
