from flask import Flask,render_template
from Member import *
from User import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "sattawat"
app.permanent_session_lifetime = timedelta(days=1)
app.register_blueprint(member)
app.register_blueprint(user)

@app.route("/")
def Index():
    return "This is home"
    #return render_template('index.html',headername="แสดงข้อมูลสมาชิก")

if __name__ == '__main__':
    app.run(debug = True)
