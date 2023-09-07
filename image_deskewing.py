import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

# from img_preperation import display


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

    angles = []

    # Loop through each contour and find the angle of the bounding box
    for contour in contours:
        minAreaRect = cv2.minAreaRect(contour)

        # Determine the angle. Convert it to the value that was originally used to obtain the skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = 90 + angle

        angles.append(-1.0 * angle)

    # Gets a mean value of angle from detected boxes
    one_angle = 0
    subtract_if_0 = 0
    print("List of angles ", angles[:])
    for one_angle in angles:
        if one_angle == 0 or one_angle == 0.0:
            subtract_if_0 += 1

    sum_of_angles = sum(angles)
    print("Sum of angles", sum_of_angles)
    print("lenght of list ", len(angles), "and the number to subtract", subtract_if_0)
    ang_to_return = sum_of_angles / (len(angles) - subtract_if_0)
    print("after devision", ang_to_return + 90)
    angles.sort()
    print(angles[0])
    return ang_to_return + 90


# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    img = cv2.imread(cvImage)

    # Get the image's height and width
    height, width = img.shape[:2]

    # Calculate the rotation center
    center = (width // 2, height // 2)

    # Get the rotation matrix using cv2.getRotationMatrix2D
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Calculate the bounding box of the rotated image
    cos_angle = np.abs(rotation_matrix[0, 0])
    sin_angle = np.abs(rotation_matrix[0, 1])
    new_width = int((height * sin_angle) + (width * cos_angle))
    new_height = int((height * cos_angle) + (width * sin_angle))

    # Adjust the rotation matrix to take into account the new size
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]

    # Perform the rotation using cv2.warpAffine
    rotated_img = cv2.warpAffine(img, rotation_matrix, (new_width, new_height), flags=cv2.INTER_CUBIC,
                                 borderMode=cv2.BORDER_REPLICATE)

    return rotated_img


# Deskew image
def deskew(cvImage):
    angle = get_skew_angle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)


def runt_test(many):
    if many == 1:
        for x in os.listdir("lore_ipsum_skewed"):
            if x.endswith(".png"):
                rotated_image = f"lore_ipsum_skewed/{x}"
                #print(get_skew_angle(rotated_image))
                fixed_image = deskew(rotated_image)
                # display(rotated_image)
                fixed_image = cv2.rotate(fixed_image, cv2.ROTATE_90_CLOCKWISE)

                cv2.imwrite(f'fixed_lore_ipsum/{x}', fixed_image)
    elif many == 2:
        for x in os.listdir("lore_ipsum_skewed"):
            if x.endswith(".png"):
                rotated_image = f"lore_ipsum_skewed/{x}"
                print(get_skew_angle(rotated_image))
    else:
        rotated_im = 'lore_ipsum_skewed/skew_lore_ipsum1.png'
        print(get_skew_angle(rotated_im))


def run_deskew_again():
    for x in os.listdir("fixed_lore_ipsum"):
        if x.endswith(".png"):
            angle = get_skew_angle(f"fixed_lore_ipsum/{x}")
            print(get_skew_angle(f"fixed_lore_ipsum/{x}"), end=" ")
            print(x)

            image = rotateImage(f"fixed_lore_ipsum/{x}", angle=(angle * -1.0))
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(f"fixed_lore_ipsum/{x}", image)


if __name__ == '__main__':


    #runt_test(many=1)
    #run_deskew_again()

    image = cv2.imread("fixed_lore_ipsum/skew_lore_ipsum0.png")
    im_str = "lore_ipsum_skewed/skew_lore_ipsum4.png"
    im_read = 'rotated_img.png'
    get_skew_angle(im_read)
    cv2.imwrite("test_new_deskew.png", deskew(im_str))
