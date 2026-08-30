from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import db

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/registration', methods=['POST'])
def registr():
    username = request.form['username']
    password = request.form['password']
    if username == " " or password == " ":
        return render_template('registration.html')
    else:
        db.reg_user(username, password)
        return "registration successful"

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == " " or password == " ":
        return render_template('login.html')
    else:
        user = db.get_user(username)
        if user:
            if username == user[1] and password == user[2]:
                session['user'] = username
                return render_template("profile.html", username=username, avatar=user[3])
            else:
                return render_template('login.html')
        else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/editprofile')
def editprofile():
    return render_template('editprofile.html')

@app.route('/editprofile', methods=["GET", 'POST'])
def editcheck():
    username = request.form['username']
    old_password = request.form['old_password']
    newpassword = request.form['new_password']
    avatar = request.form['avatar']
    user = db.get_user(session.get('user'))
    if old_password == "" or newpassword == "" or username == "":
        return render_template('editprofile.html')
    if old_password == user[2]:
        db.edit_user(username, newpassword, session['user'],  avatar)
        session['user'] = username
        return render_template('profile.html', username=username, avatar=user[3])
    else:
        return render_template('editprofile.html')

@app.route("/dashboard")
def dashboard():
    messages = db.getMessages()
    return render_template('dashboard.html', messages = messages)

@app.route("/add_message", methods=['GET', 'POST'])
def add_message():
    message_text = request.form['text']
    if message_text == "":
        messages = db.getMessages()
        return render_template('dashboard.html', messages = messages)
    else:
        user = db.get_user(session['user'])
        if user is None:
            return render_template('login.html')
        else:
            db.saveMessages(user[0], message_text)
            messages = db.getMessages()
            return render_template('dashboard.html', messages = messages)

@app.route("/deleteuser")
def Deleteuser():
    if "user" not in session:
        return redirect('/login')
    db.deleteuser(session['user'])
    session['user'] = None
    return redirect('/login')


port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True)