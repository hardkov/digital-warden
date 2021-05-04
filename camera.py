import cv2
import base64
import threading
from time import sleep

from detection import detectHuman


socket = None
camera = None
capturingBlocked = False
currentHumanCount = 0

def initializeCamera(socketio):
    global camera
    global socket

    socket = socketio

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera = cv2.VideoCapture(1)

def closeCamera():
    camera.release()
    cv2.destroyAllWindows()

def unlockCapture(timeout):
    global capturingBlocked

    sleep(timeout)
    capturingBlocked = False

def gen_frames():
    global currentHumanCount, capturingBlocked

    while True:
        success, frame = camera.read()
        if not success:
            break
        
        frame, count = detectHuman(frame)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        if count > currentHumanCount and not capturingBlocked:
            capturingBlocked = True
            
            socket.emit("imgFeed", base64.b64encode(buffer).decode("utf-8"))
            
            threading.Thread(target=unlockCapture, args=(2, )).start()

        currentHumanCount = count

        socket.emit("countFeed", count)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
