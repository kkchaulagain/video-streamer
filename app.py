from flask import Flask, Response, render_template
import cv2
import threading

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

camera = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def generate():
    global outputFrame, lock
    while True:
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def read_frame():
    global camera, outputFrame, lock
    while True:
        ret, frame = camera.read()
        with lock:
            outputFrame = frame.copy()

t = threading.Thread(target=read_frame)
t.daemon = True
t.start()

if __name__ == '__main__':
    from gunicorn.app.wsgiapp import run
    run()
