# coding=utf-8
import numpy as np
import cv2


def findFaces(imagePath, imageDebug=False):
    """
    find faces on photo given by input path and returns number of detected faces.
    :param imagePath: path to image
    :param imageDebug: if True, open image with detected faces in detached window
    :return:
    """
    face_cascade = cv2.CascadeClassifier(r'.\cascades\haarcascade_frontalface_default.xml')

    img = cv2.imread(imagePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if imageDebug:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        res = cv2.resize(img, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_CUBIC)
        cv2.imshow('detection', res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return len(faces)


if __name__ == "__main__":
    print("Number of faces detected on test picture: {}".format(findFaces(r".\test_images\test_image.jpg")))
