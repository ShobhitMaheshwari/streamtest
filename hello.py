from flask import Flask, render_template, Response
from flask_socketio import SocketIO, join_room, emit
import cv2

app = Flask(__name__, template_folder='.')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

#not used currently
@app.route('/get')
def get(x):
    print(x)

#not used currently
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@socketio.on('create')
def on_create(data):
    print(data)
    #data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY) # need to first decode from base64
    emit('join_room', data) # emit data back as it is


if __name__ == '__main__':
    #app.run()
    socketio.run(app, debug=True)
