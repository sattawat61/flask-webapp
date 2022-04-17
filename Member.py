from flask import Blueprint,render_template,request,redirect,url_for,session
import pymysql
from config import *
import os

con = pymysql.connect(HOST,USER,PASS,DATABASE)
member = Blueprint('member',__name__)

@member.route("/showdatamembersomeone",methods=["POST"])
def Showsomeone():
    if "username" not in session:
        return render_template('login.html',headername="Login เข้าใช้งานระบบ")
    if request.method == "POST":
        id = request.form["id"]
        with  con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_member where mem_id = %s"
            cur.execute(sql,(id))
            rows = cur.fetchall()
            return render_template("showdatamebersomeone.html",headername="ข้อมูลสมาชิก",datas=rows)

@member.route("/showmember")
def Showdatamember():
    if "username" not in session:
        return render_template('login.html',headername="Login เข้าใช้งานระบบ")
    with  con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_member"
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template("Showdatamember copy.html",headername="ข้อมูลสมาชิก",datas=rows)

@member.route("/showwithdate",methods=["POST"])
def Showwithdate():
    if "username" not in session:
        return render_template('login.html',headername="Login เข้าใช้งานระบบ")
    if request.method == "POST":
        dtstart = request.form['dtstart']
        dtend = request.form['dtend']
        with  con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_member where mem_datetimestamp between %s and %s "
            cur.execute(sql,(dtstart,dtend))
            rows = cur.fetchall()
            return render_template("Showdatamember.html",headername="ข้อมูลสมาชิก",datas=rows)


@member.route("/editmember",methods=["POST"])
def Editmember():
    if request.method == "POST":

        id = request.form["id"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        file = request.files['files']
        if file.filename =="":
            #update with no pic
            with con :
                cur = con.cursor()
                sql = "update tb_member set mem_fname = %s,mem_lname = %s,mem_email = %s where mem_id = %s"
                cur.execute(sql,(fname,lname,email,id))
                con.commit()
                return redirect(url_for('member.Showdatamember'))
        else:
                #update with pic
                file = request.files['files']
                upload_folder = 'static/images'
                app_folder = os.path.dirname(__file__)
                img_folder = os.path.join(app_folder,upload_folder)
                file.save(os.path.join(img_folder,file.filename))
                path = upload_folder + "/" + file.filename
                with con :
                    cur = con.cursor()
                    sql = "update tb_member set mem_fname = %s,mem_lname = %s,mem_email = %s, mem_pic = %s where mem_id = %s"
                    cur.execute(sql,(fname,lname,email,path,id))
                    con.commit()
                    return redirect(url_for('member.Showdatamember'))

@member.route("/delmember",methods=["POST"])
def Delmember():
    if request.method == "POST":
        id = request.form['id']
        with con :
            cur = con.cursor()
            sql = "delete from tb_member where mem_id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for('member.Showdatamember'))

@member.route("/adddatamember")
def Adddatamember():
    return render_template("adddatamember.html",headername="เพิ่มข้อมูลสมาชิก")

@member.route("/adddata",methods=["POST"])
def Adddata():
    if request.method == "POST":
        file = request.files['files']
        upload_folder = 'static/images'
        app_folder = os.path.dirname(__file__)
        img_folder = os.path.join(app_folder,upload_folder)
        file.save(os.path.join(img_folder,file.filename))
        path = upload_folder + "/" + file.filename

        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        with con :
            cur = con.cursor()
            sql = "insert into tb_member (mem_fname,mem_lname,mem_email,mem_pic) VALUES (%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,email,path))
            con.commit()
            return redirect(url_for('member.Showdatamember'))
