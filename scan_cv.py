from unittest import result
import cv2, pytesseract

SCALE = 4
AREA_THRESHOLD = 427505.0 / 2

def show_scaled(name, img):
    try:
        h, w  = img.shape
    except ValueError:
        h, w, _  = img.shape
    cv2.imshow(name, cv2.resize(img, (w // SCALE, h // SCALE)))

filename = 'tmp/page_1.jpg'

def scanCV(image):
    # Load image, grayscale, Gaussian blur, Otsu's threshold
    #image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (23,23), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=20)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    index = 0
    result = ''
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

        cropped = image[y :y +  h , x : x + w]
        #s = 'tmp/crop_' + str(index) + '.jpg' 
        #cv2.imwrite(s , cropped)
        result += str(((pytesseract.image_to_string(cropped, lang='vie',config='--oem 1')))).strip() + '\n'
        index = index + 1

    #(1260,1782)
    cv2.imshow('thresh', cv2.resize(thresh, (1240,874)))
    cv2.imshow('dilate', cv2.resize(dilate,(1240,874)))
    cv2.imshow('image', cv2.resize(image, (1240,874)))
    cv2.waitKey()

    return result