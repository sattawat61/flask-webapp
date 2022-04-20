<<<<<<< HEAD
from tkinter import Frame
from flask import Flask,render_template,Response
import cv2
import tensorflow as tf
import numpy as np
from Member import *
from User import *
from datetime import timedelta
###############
from facemaskdetection_2 import stream



app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = stream()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')





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
    return Response(gen_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug = True)
=======
from flask import Flask,render_template,Response
import cv2
import tensorflow as tf
import numpy as np
from Member import *
from User import *
from datetime import timedelta
###############



app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
            
        #read the cameraframe
        success,frame=camera.read()
        if not success:
            break
        else:
            face_mask = ['Masked', 'No mask']
            size = 224

            # Load face detection and face mask model
            path = r'D:/project/Flaskmyweb - Copy - test/face_mask.model'
            model = tf.keras.models.load_model(os.path.join(path, 'D:/project/Flaskmyweb - Copy - test/face_mask.model'))
            faceNet = cv2.dnn.readNet(os.path.join(path, 'D:/project/Flaskmyweb - Copy - test/face_mask.model', 'D:/project/Flaskmyweb - Copy - test/face_mask.model/face_detect/deploy.prototxt.txt'),
                                    os.path.join(path, 'D:/project/Flaskmyweb - Copy - test/face_mask.model', 'D:/project/Flaskmyweb - Copy - test/face_mask.model/face_detect/res10_300x300_ssd_iter_140000.caffemodel'))

            cap = cv2.VideoCapture(0)
            #cap = cv2.VideoCapture(os.path.join(path, 'face_mask4.mp4'))
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            out = cv2.VideoWriter(os.path.join(path, 'test4.avi'),
                                cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width, frame_height))
            while True:
                ret, frame = cap.read()
                (h, w) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
                faceNet.setInput(blob)
                detections = faceNet.forward()

                for i in range(0, detections.shape[2]):
                    confidence = detections[0, 0, i, 2]

                    if confidence < 0.5:
                        continue

                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype('int')
                    (startX, startY) = (max(0, startX), max(0, startY))
                    (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
                    face = frame[startY:endY, startX:endX]
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                    face = cv2.resize(face, (size, size))
                    face = np.reshape(face, (1, size, size, 3)) / 255.0
                    result = np.argmax(model.predict(face))

                    if result == 0:
                        label = face_mask[result]
                        color = (0, 255, 0)
                    else:
                        label = face_mask[result]
                        color = (0, 0, 255)

                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 3)
                    cv2.rectangle(frame, (startX, startY - 60), (endX, startY), color, -1)
                    cv2.putText(frame, label, (startX + 10, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

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
>>>>>>> 676728eb719120ba537b592913578efa8d88ef5f
