import cv2
import matplotlib.pyplot

from img_preperation import display


# Calculate skew angle of an image
def get_skew_angle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cv2.imread(cvImage)
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilation to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Find the largest contour and surround in min area box
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle


# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cv2.imread(cvImage)
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage


# Deskew image
def deskew(cvImage):
    angle = get_skew_angle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)


if __name__ == '__main__':
    rotated_image = 'rotated_img.png'
    print(get_skew_angle(rotated_image))
    fixed_image = deskew(rotated_image)
    display(rotated_image)
    fixed_image = cv2.rotate(fixed_image, cv2.ROTATE_90_CLOCKWISE)

    cv2.imwrite('fixed_the_skew.png', fixed_image)
