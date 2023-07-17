"""Progaram to OCR from images png/jpg"""
import time
from PIL import Image
import cv2
import pytesseract
import matplotlib.pyplot as plt
import numpy as np
import threading
import os


def change_rgba_value(loaded_image):
    # image size 780 x 787 x 4

    arrayed_image = np.array(loaded_image)
    fig, ax = plt.subplots()

    for x, row in enumerate(arrayed_image):
        for y, column in enumerate(row):
            for z, rgba in enumerate(column):
                if (rgba == 0) & (z != 4):
                    arrayed_image[x, y, z] = 255
                elif (rgba == 255) & (z != 4):
                    arrayed_image[x, y, z] = 0
    ax.imshow(arrayed_image)
    cv2.imwrite('temp/inverted.png', arrayed_image)
    plt.show()


def display(im_path):
    """displays the file in matplotlib.
    it accepts path to image as a attribute"""
    dpi = 80
    if os.path.exists(im_path):
        im_data = cv2.imread(im_path)
    else:
        im_data = cv2.imshow("image", im_path)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    try:
        height, width, depth = im_data.shape
    except ValueError:
        print("not enough values to unpack (expected 3, got 2)")
        height, width = im_data.shape

    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    ax.axis('off')

    ax.imshow(im_data, cmap='gray')
    plt.show()


def to_gray_scale(image):
    """converts the image to a gray scale"""
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def noise_removal(image):
    """reduces the image noise to adjust play with iterations and the ones attributes"""
    kernal = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernal, iterations=1)
    kernal = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernal, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernal)
    image = cv2.medianBlur(image, 1)
    return image


def thin_font(image):
    """erodes the image ergo it thins the font to adjust play with iterations and the ones attributes"""
    image = cv2.bitwise_not(image)
    kernel = np.ones((1, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


def thick_font(image):
    """id dialates the image ergo it thickens the font to adjust play with iterations and the ones attributes"""
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


if __name__ == '__main__':

    path_to_image = 'File_to_ocr.png'
    path_to_inverted_image = 'temp/inverted2.png'
    path_to_gray_image = 'temp/gray_scale.jpg'
    path_to_bw_image = 'temp/bw_image.jpg'
    img = cv2.imread(path_to_image)
    # change_rgba_value(img)
    # display(path_to_image)

    # inverted_image = cv2.bitwise_not(img)
    # cv2.imwrite("temp/inverted2.png", inverted_image)
    # display(path_to_inverted_image)

    # gray_image = to_gray_scale(img)
    # cv2.imwrite('temp/gray_scale.jpg', gray_image)
    # print(np.array(cv2.imread(path_to_gray_image)))
    # display(path_to_gray_image)
    # thresh, im_bw = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    # cv2.imwrite("temp/bw_image.jpg", im_bw)
    # display(path_to_bw_image)
    no_noise = noise_removal(cv2.imread(path_to_bw_image))
    # cv2.imwrite('temp/no_noise.jpg', no_noise)
    # display('temp/no_noise.jpg')
    eroded_image = thin_font(no_noise)
    cv2.imwrite('temp/eroded_image.jpg', eroded_image)
    display('temp/eroded_image.jpg')
    # dialated_image = thick_font(no_noise)
    # cv2.imwrite('temp/thick_font.jpg', dialated_image)
    # display('temp/thick_font.jpg')
