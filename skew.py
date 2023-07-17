import  cv2


def skew_image(cvImage, angle: float):
    newImage = cv2.imread(cvImage)
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage


if __name__ == '__main__':
    image_path_to_skew = 'new_file_to_ocr.png'
    rotated_image = skew_image(image_path_to_skew, 7.5)
    cv2.imwrite('rotated_img.png', rotated_image)
