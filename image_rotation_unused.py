from typing import ClassVar
import numpy as np
import cv2
import math
from scipy import ndimage
from PIL import Image

def rotate(image_to_rotate):
    img_before = cv2.imread(image_to_rotate)

    #cv2.imshow("Before", img_before)    
    key = cv2.waitKey(0)

    img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

    angles = []

    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    #cv2.imshow("Detected lines", img_before)    
    key = cv2.waitKey(0)

    median_angle = np.median(angles)
    img_rotated = ndimage.rotate(img_before, median_angle, cval=0.0)

    print(f"Angle is {median_angle:.04f}")
    cv2.imwrite(image_to_rotate, img_rotated)
    return median_angle 
    

def rotate_1(image_to_rotate, angle):

    img = Image.open(image_to_rotate)
    img = img.rotate(angle=angle, expand=True, resample=Image.NEAREST, fillcolor='white')
    img.show()



#https://stackoverflow.com/questions/46731947/detect-angle-and-rotate-an-image-in-python/46732132
#print('before rotation')
#angle = rotate('static/uploads/00000024.jpg')
#rotate_1('static/uploads/00000024.jpg', -90)
#print('after rotation')
