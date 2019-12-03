from flask import Flask, render_template, Response
from flask_socketio import SocketIO, join_room, emit
import cv2
import base64
import numpy as np

app = Flask(__name__, template_folder='.')
socketio = SocketIO(app)

def readb64(encoded_data):
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #sbuf = StringIO()
    #sbuf.write(base64.b64decode(base64_string))
    #pimg = Image.open(sbuf)
    #return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

@app.route('/')
def index():
    return render_template('index.html')

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
    
    x = len('data:image/png;base64,')
    image = readb64(data[x:])
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    g = np.array(cv2.imencode('.jpg', image)[1]).tostring()
    print(g)
    r = x+base64.b64encode(g)

    emit('join_room', r) # emit data back as it is


if __name__ == '__main__':
    #app.run()
    socketio.run(app, debug=True)
