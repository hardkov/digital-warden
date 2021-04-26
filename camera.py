import cv2
import base64

from detection import detectHuman

socket = None
camera = None
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

def gen_frames():
    global currentHumanCount

    while True:
        success, frame = camera.read()
        if not success:
            break
        
        frame, count = detectHuman(frame)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        if count > currentHumanCount:
            # save image and send to the client
            print("imgFeed")
            socket.emit("imgFeed", base64.b64encode(buffer))

        currentHumanCount = count

        socket.emit("countFeed", count)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
