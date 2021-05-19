from flask import Flask, render_template, Response, jsonify, make_response
from flask_socketio import SocketIO

from camera import initialize_camera, close_camera, gen_frames
from storage import get_saved_frames, close_database, initialize_database
from helpers import parse_frames

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    saved_frames = get_saved_frames(-1)
    frames_by_days = parse_frames(saved_frames)

    return render_template('data.html', frames_by_days=frames_by_days)

@app.route('/')
def index():
    frames_limit = 5

    saved_frames = get_saved_frames(frames_limit)

    return render_template('index.html', frames_limit=frames_limit, frames_count=len(saved_frames), saved_frames=saved_frames)

if __name__ == '__main__':
    initialize_database()
    initialize_camera(socketio)

    socketio.run(app)

    close_camera()
    close_database()