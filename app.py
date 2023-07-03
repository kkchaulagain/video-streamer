import subprocess
from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # use 0 for web camera

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/hls_stream.m3u8')
def hls_stream():
    # Run FFmpeg command to convert frames to video
    cmd = [
        'ffmpeg', '-f', 'image2pipe', '-framerate', '30', '-i', '-',
        '-vf', 'format=yuv420p', '-c:v', 'libx264', '-f', 'hls', '-'
    ]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # Stream the output of FFmpeg process
    return Response(p.stdout, mimetype='application/vnd.apple.mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
