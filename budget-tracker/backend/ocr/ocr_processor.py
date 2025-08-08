import pytesseract
import cv2
from PIL import Image
import os

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    # Upscale to help OCR pick digits
    img = cv2.resize(img, None, fx=1.7, fy=1.7, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise + enhance contrast
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 31, 4)

    # Optional: slight dilation to connect broken digits
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=1)

    temp_filename = "temp_receipt.png"
    cv2.imwrite(temp_filename, gray)

    # PSM 6: assume a block of text; OEM 3: LSTM
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(Image.open(temp_filename), config=config)

    os.remove(temp_filename)
    return text
