import cv2
import random
import os
import matplotlib.pyplot as plt
import numpy as np


def skew_image(image_path, angle: float):
    # Load the image using OpenCV
    img = cv2.imread(image_path)

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
    rotated_img = cv2.warpAffine(img, rotation_matrix, (new_width, new_height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated_img


if __name__ == '__main__':

    for x in os.listdir("lore_ipsum_text_gen"):
        if x.endswith(".png"):
            print(x)
            skew_angle = random.uniform(1.0, 20.0)
            print(skew_angle)
            image_path_to_skew = f'lore_ipsum_text_gen/{x}'
            rotated_image = skew_image(image_path_to_skew, skew_angle)
            cv2.imwrite(f'lore_ipsum_skewed/skew_{x}', rotated_image)
