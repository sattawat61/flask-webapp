from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import pymysql
from config import *

con = pymysql.connect(HOST,USER,PASS,DATABASE)
user = Blueprint('user',__name__)

@user.route("/live")
def live():
        return render_template("live.html",headername="Login เข้าใช้งานระบบ")


@user.route("/loginpage")
def Loginpage():
    if "username" not in session:
        return render_template("login.html",headername="Login เข้าใช้งานระบบ")
    else:
        return redirect(url_for('member.Showdatamember'))

@user.route("/checklogin",methods=["POST"])
def Checklogin():
    username = request.form['username']
    password = request.form['password']
    with  con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_user WHERE usr_username = %s AND usr_password = %s AND usr_status=1 "
        cur.execute(sql,(username,password))
        rows = cur.fetchall()
        print("จำนวนเเถวในการเจอข้แมูล = "+ str(len(rows)))
        if len(rows) > 0:
            session['username'] = username
            session['Firstname'] = rows[0][1]
            session['Lastname'] = rows[0][2]
            session.permanent = True
            print(session)
            return redirect(url_for('member.Showdatamember'))
        else:
            flash("ไม่พบข้อมูลในระบบ")
            return render_template('login.html',headername="Login เข้าใช้งานระบบ")

@user.route("/logout")
def logout():
    session.clear()
    print(session)
    return redirect(url_for('user.Loginpage'))

@user.route("/regisuser")
def Regisuser():
    return render_template('adduser.html',headername="สมัครสมาชิก")

@user.route("/adduser",methods=["POST"])
def Adduser():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        username = request.form["username"]
        password = request.form["password"]
        repassword = request.form["repassword"]
        if password != repassword:
            flash("คุณกรอก password และ Re-password ไม่ตรงกัน")
            return render_template('adduser.html',headername="สมัครสมาชิก")


        with con :
            cur = con.cursor()
            sql = "insert into tb_user (usr_fname,usr_lname,usr_username,usr_password) values (%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,username,password))
            con.commit()
            flash("สมัครสมาชิกสำเร็จรอผู้ดูเเลตรวงสอบ")
            return render_template('login.html',headername="สมัครสมาชิก",status="wait")
