import os as os
from flask import Flask, render_template, request, session, redirect
import pymysql
import db_methods
import datetime as dt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a27'


def authcheck():
    if 'user_id' in session:
        return True
    else:
        return False


@app.route('/')
def hello():
    if 'user_id' in session:
        return render_template('my_songs.html', songs=db_methods.get_songs_of_users(int(session['user_id'])))
    else:
        return redirect('/login')


@app.route('/login')
def loginPage():
    return render_template('login.html')


@app.route('/home', methods=["POST", "GET"])
def loginSignin():
    username = request.form["loginEmail"]
    password = request.form["loginPassword"]
    login = db_methods.login_authentication(username, password)
    if login:
        session['user_id'] = login
        print(session['user_id'])
        return render_template('my_songs.html', songs=db_methods.get_songs_of_users(int(session['user_id'])))
    else:
        return render_template('login.html', message1="Email or Password Incorrect")


@app.route('/signIn', methods=["POST", "GET"])
def signIn():
    name = request.form["name"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    gender = request.form["gender"]
    user_type = request.form["user_type"]
    signIn = db_methods.create_user(email, name, lastname, gender, username, password, 0, dt.datetime(2000, 2, 3))
    if signIn:
        session['user_id'] = str(signIn)
        return render_template('my_songs.html', songs=db_methods.get_songs_of_users(int(session['user_id'])))
    else:
        return render_template('login.html', message2="Username or Email Exist")


@app.route('/mysongs')
def mySons():
    if authcheck():
        return render_template('my_songs.html', songs=db_methods.get_songs_of_users(int(session['user_id'])))
    else:
        return redirect('/')

@app.route('/market')
def market():
    if authcheck():
        return render_template('market.html', songs=db_methods.get_songs_by_most_listened(),
                           albums=db_methods.get_albums_by_most_listened())
    else:
        return redirect('/')


@app.route('/buyalbum', methods=["POST", "GET"])
def buyalbum():
    if authcheck():
        album_id = request.args.get('id')
        message = db_methods.purchase_album(session['user_id'], album_id)
        return redirect('/market?message=' + message + '')
    else:
        return redirect('/')

@app.route('/buysong', methods=["POST", "GET"])
def buysong():
    if authcheck():
        song_id = request.args.get('id')
        message = db_methods.purchase_song(session['user_id'], song_id)
        return redirect('/market?message=' + message + '')
    else:
        return redirect('/')

@app.route('/timeline')
def timeline():
    if authcheck():
        return render_template('timeline.html')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


if __name__ == '__main__':
    app.run()
