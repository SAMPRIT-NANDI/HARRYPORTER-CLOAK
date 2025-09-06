import cv2
import time
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))   

cap = cv2.VideoCapture(0)

time.sleep(3)
background = 0  
for i in range(60):
    ret, background = cap.read()
background = np.flip(background, axis=1)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = np.flip(img, axis=1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Maroon/Dark Magenta color range in HSV
    lower_maroon = np.array([160, 100, 20])
    upper_maroon = np.array([180, 255, 150])
    mask = cv2.inRange(hsv, lower_maroon, upper_maroon)

    # Morphological operations to clean mask
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=2)

    # Smooth mask edges
    mask = cv2.GaussianBlur(mask, (15, 15), 0)

    mask_inv = cv2.bitwise_not(mask)

    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(img, img, mask=mask_inv)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    out.write(final_output)
    cv2.imshow('Magic', final_output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()