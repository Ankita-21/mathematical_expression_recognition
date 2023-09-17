import os
import cv2
import numpy as np
import pytesseract
import tensorflow as tf
import matplotlib.pyplot as ptl
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# Path of working folder on Disk
src_path = "image/"

# Tessdata path
os.environ['TESSDATA_PREFIX'] = 'C:/Program Files/Tesseract-OCR/tessdata'


def get_string(img_path, tub_kernel):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones(tub_kernel, np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    gray = cv2.erode(gray, kernel, iterations=2)

    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", gray)

    #  Apply threshold to get image with only black and white
    _, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "thres.png", gray)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))

    return result


print('START RECOGNIZE MATCH')
img_path = src_path + "vol.jpeg"

# Extract text from image
result = get_string(img_path, (2,3)).strip()

#Try one more
if not result or len(result.split(" ")) < 5:
    result = get_string(img_path, (1, 3))

# Try one more
if not result or len(result.split(" ")) < 5:
    result = get_string(img_path, (4, 3))

print("TEXT RESULT:")
print(result)

print("EXTRACT EXPRESSION")
# Split using space
data = result.strip().split(" ")
for num in data:
    print(num)

print("Done")