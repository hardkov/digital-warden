import numpy as np
import cv2
 
classifier = cv2.HOGDescriptor()
classifier.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect_human(frame):
    frame = cv2.resize(frame, (640, 480))

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    boxes, _ = classifier.detectMultiScale(gray, winStride=(8, 8))

    try:
        human_count = boxes.shape[0]
    except:
        human_count = 0

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
    
    return frame, human_count