from flask import Flask, render_template, Response
from flask_socketio import SocketIO

from camera import initializeCamera, closeCamera, gen_frames

app = Flask(__name__)
socketio = SocketIO(app)

initializeCamera(socketio)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)

closeCamera()