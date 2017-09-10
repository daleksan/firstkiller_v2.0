# coding=utf-8
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier(r'.\cascades\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(r'.\cascades\haarcascade_eye.xml')

img = cv2.imread('test_photo.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

res = cv2.resize(img, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_CUBIC)
cv2.imshow('detection', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
