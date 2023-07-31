import pytesseract
from PIL import Image


img_file = "new_file_to_ocr.png"
img_file2 = 'File_to_ocr.png'
img_file3 = "fixed_lore_ipsum/skew_lore_ipsum1.png"
img_file4 = "Screenshot_2023-07-25_13-52-44.png"

img = Image.open(img_file2)

ocr_result = pytesseract.image_to_pdf_or_hocr(img_file4, extension='pdf', lang="pol")
ocr_result2 = pytesseract.image_to_string(img_file3, lang="pol")


if __name__ == '__main__':
    print(ocr_result)
    with open('ocr_topdf.pdf', 'wb') as file:
        file.write(ocr_result)
    with open('ocr_to_txt.txt', "w") as file2:
        file2.write(ocr_result2)
