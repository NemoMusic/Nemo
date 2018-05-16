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

@app.route('/profile')
def profile():
    if authcheck():
        id = request.args.get('username')
        if id is None:
            uid=int(session['user_id'])
            return render_template('profile.html', user=db_methods.get_User(uid),created=db_methods.get_users_playlists(uid),
                                   followed=db_methods.get_following_playlist(uid),followers=db_methods.get_followers(uid),
                                   followings=db_methods.get_following_playlist(uid), events=db_methods.get_attended_events(uid))
        else:
            uid = db_methods.get_userid_by_username(id)
            return render_template('profile.html', user=db_methods.get_User(uid),
                                   created=db_methods.get_users_playlists(uid),
                                   followed=db_methods.get_following_playlist(uid),
                                   followers=db_methods.get_followers(uid),
                                   followings=db_methods.get_following_playlist(uid),
                                   events=db_methods.get_attended_events(uid))

    else:
        return redirect('/')


@app.route('/buyalbum', methods=["POST", "GET"])
def buyalbum():
    if authcheck():
        album_id = request.args.get('id')
        message = db_methods.purchase_album(session['user_id'], album_id)
        return redirect('/market?message=' + message + '')
        return redirect('/')

@app.route('/market')
def market():
    if authcheck():
        return render_template('market.html', songs=db_methods.get_songs_by_most_listened(),
                               albums=db_methods.get_albums_by_most_listened())
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
        uid = session['user_id']
        return render_template('timeline.html',activities=db_methods.timeline_message(uid))
    else:
        return redirect('/')

@app.route('/search', methods=["POST", "GET"])
def search():
    if authcheck():
        searchkey = request.args.get('key')
        songs = db_methods.search_song(searchkey)
        albums = db_methods.search_album(searchkey)
        events = db_methods.search_events(searchkey)
        users = db_methods.search_user(searchkey)
        return render_template('aftersearch.html',users=users, songs= songs, albums=albums, events=events, search_key=searchkey)
    else:
        return redirect('/')

@app.route('/playlists')
def playlists():
    if authcheck():
        id = request.args.get('id')
        return render_template('playlists.html', songs=db_methods.get_songs_of_playlist(id))
    else:
        return redirect('/')

@app.route('/events')
def events():
    if authcheck():
        return render_template('events.html', events=db_methods.get_all_events())
    else:
        return redirect('/')


@app.route('/delete')
def delete():
    id = request.args.get('id')
    uid = int(session['user_id'])
    db_methods.delete_user_song(uid,int(id))
    return redirect('/mysongs')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


@app.route('/attend')
def attend():
    id = int(request.args.get('id'))
    uid = int(session['user_id'])
    message = db_methods.user_attend_to_event(uid,id)
    return redirect('/events?message=' + message)

@app.route('/createPlaylist')
def createPlaylistPage():
    return render_template('create_playlist.html')

if __name__ == '__main__':
    app.run()
