import os as os
from flask import Flask, render_template, request, session, redirect
import pymysql

app = Flask(__name__)


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
    return render_template('welcome.html')




if __name__ == '__main__':
    app.run()