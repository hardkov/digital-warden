import numpy as np
import cv2
 
classifier = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')

def detectHuman(frame):
    frame = cv2.resize(frame, (640, 480))

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    boxes = classifier.detectMultiScale(gray, 1.3, 5)

    try:
        human_count = boxes.shape[0]
    except:
        human_count = 0

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
    
    return frame, human_count