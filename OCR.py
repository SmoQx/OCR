import pytesseract
from PIL import Image


img_file = "new_file_to_ocr.png"
img_file2 = 'File_to_ocr.png'

img = Image.open(img_file2)

ocr_result = pytesseract.image_to_pdf_or_hocr(img_file2, extension='pdf')


if __name__ == '__main__':
    print(ocr_result)
    with open('ocr_topdf.pdf', 'wb') as file:
        file.write(ocr_result)
