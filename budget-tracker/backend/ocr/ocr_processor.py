import pytesseract
import cv2
from PIL import Image
import os

def extract_text_from_image(image_path):
    # Read and preprocess image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # Save temp file
    temp_filename = "temp_receipt.png"
    cv2.imwrite(temp_filename, gray)

    # Extract text
    text = pytesseract.image_to_string(Image.open(temp_filename))

    # Clean up
    os.remove(temp_filename)
    return text
