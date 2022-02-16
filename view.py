from flask import Flask,render_template,Response
import cv2
from Member import *
from User import *
from datetime import timedelta

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
            
        #read the cameraframe
        success,frame=camera.read()
        if not success:
            break
        else:
            
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'+ frame +b'\r\n')


app.secret_key = "sattawat"
app.permanent_session_lifetime = timedelta(days=1)
app.register_blueprint(member)
app.register_blueprint(user)

@app.route("/")
def Index():
    # return "This is home"
    return render_template('login.html',headername="Login เข้าใช้งานระบบ")

@app.route("/test")
def index1():
    return render_template('test.html',)

@app.route("/video")
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug = True)
