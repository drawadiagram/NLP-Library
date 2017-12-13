# OCR a some files and throw em into text

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import os
import time

my_orig_pdf = '/home/mason/topics/historyofswedish01stra.pdf'
my_output = '/home/mason/topics/my_ocr_text.txt'

tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[1]

def ocr_pdf(pdf_to_ocr, output_file):
    req_image = []
    final_text = []

    image_pdf = Image(filename=pdf_to_ocr, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')

    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))

    for img in req_image:
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt)

    with open(output_file, 'a+') as f:
        for text in final_text:
            f.write(text)

docname = os.path.basename(os.path.splitext(my_orig_pdf)[0])
docdir = os.path.dirname(os.path.abspath(my_orig_pdf))
files_list = os.listdir(os.path.join(docdir,docname))
files_list.sort()

bigstart = time.time()
for item in files_list:
    start = time.time()
    ocr_pdf(os.path.join(docdir,docname,item), my_output)
    stop = time.time()
    print("runtime %.03f" % (stop-start) + " seconds")
    temps = os.listdir('/tmp')
    for temp in temps:
        if temp.startswith('magick-'):
            os.remove(os.path.join('/tmp',temp))
bigstop = time.time()
print("total runtime %.03f" % (bigstop-bigstart) + " seconds")
