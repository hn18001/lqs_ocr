import cv2
import numpy as np
import os
from PIL import Image

def rotate_img(file_name):
    img = Image.open(file_name)
    rotate_img = img.rotate(90, expand = 1)
    rotate_img.save(file_name)

def add_border(file_name):
    height = 130
    width = 800

    white_img = np.ones((height, width, 3), np.uint8) * 255

    src_img = cv2.imread(file_name)

    src_height, src_width, src_channels = src_img.shape

    print src_width, src_height
    if src_height > height or src_width > width:
        return

    print width, height, src_width, src_height, src_channels
    width_range = range((width-src_width)/2, (width+src_width)/2)
    height_range = range((height-src_height)/2, (height+src_height)/2)
    try:
        white_img[(height-src_height)/2:(height+src_height)/2, (width-src_width)/2:(width+src_width)/2,:] = src_img
    except:
        return

    cv2.imwrite(file_name, white_img)


if __name__ == "__main__":
    path = "./img/"
