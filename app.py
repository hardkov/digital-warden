from flask import Flask, render_template, Response, jsonify, make_response
from flask_socketio import SocketIO

from camera import initialize_camera, close_camera, gen_frames
from storage import get_saved_frames

app = Flask(__name__)
socketio = SocketIO(app)

initialize_camera(socketio)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    saved_frames = get_saved_frames()

    return render_template('data.html', saved_frames=saved_frames)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/saved')
# def saved():
#     data = get_saved_frames()

#     return make_response(jsonify(data), 200)

if __name__ == '__main__':
    socketio.run(app)

close_camera()