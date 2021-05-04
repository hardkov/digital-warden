import cv2
import base64
import threading
from datetime import datetime
from time import sleep

from detection import detect_human
from storage import save_frame


socket = None
camera = None
capturing_blocked = False
current_human_count = 0

def initialize_camera(socketio):
    global camera, socket

    socket = socketio

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera = cv2.VideoCapture(1)

def close_camera():
    camera.release()
    cv2.destroyAllWindows()

def unlock_capture(timeout):
    global capturing_blocked

    sleep(timeout)
    capturing_blocked = False

def gen_frames():
    global current_human_count, capturing_blocked

    while True:
        success, frame = camera.read()
        if not success:
            break
        
        frame, count = detect_human(frame)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        buffer_encoded = base64.b64encode(buffer).decode("utf-8")
        
        if count > current_human_count and not capturing_blocked:
            capturing_blocked = True
            
            socket.emit("imgFeed", buffer_encoded)
            save_frame(datetime.now(), buffer_encoded)  
            threading.Thread(target=unlock_capture, args=(2, )).start()

        current_human_count = count

        socket.emit("countFeed", count)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
