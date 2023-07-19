import cv2
import random
import os


def skew_image(cvImage, angle: float):
    newImage = cv2.imread(cvImage)
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w+50, h+50), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage


if __name__ == '__main__':

    for x in os.listdir("lore_ipsum_text_gen"):
        if x.endswith(".png"):
            print(x)
            skew_angle = random.uniform(1.0, 20.0)
            image_path_to_skew = f'lore_ipsum_text_gen/{x}'
            rotated_image = skew_image(image_path_to_skew, skew_angle)
            cv2.imwrite(f'lore_ipsum_skewed/skew_{x}', rotated_image)
