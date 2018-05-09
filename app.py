import os as os
from flask import Flask, render_template, request, session, redirect
import pymysql
import db_methods

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

@app.route('/')
def hello():
    if 'user_id' in session:
        return redirect("/home")
    else:
        return redirect('/login')

@app.route('/login')
def loginPage():
    return render_template('login.html')


@app.route('/home', methods=["POST", "GET"])
def loginSignin():
    username = request.form["loginEmail"]
    password = request.form["loginPassword"]
    login = db_methods.login_authentication(username,password)
    if login:
        session['user_id'] = login
        print(session['user_id'])
        return render_template('welcome.html')
    else:
        return render_template('login.html',message ="Email or Password Incorrect")


@app.route('/signIn', methods=["POST","GET"])
def signIn():
    name = request.form["name"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    db_methods.create_user(name)




if __name__ == '__main__':
    app.run()