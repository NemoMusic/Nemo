import pymysql
import datetime as dt
import time
import models

from models import *

connection = None

connection = pymysql.connect(host='nemo.cnj8noexhne9.eu-west-1.rds.amazonaws.com',
                             user='nemo',
                             password='nemoadmin',
                             db='nemodb')


def execute_sql(sql, type=0):
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    if type:
        return cursor.fetchall()
    return cursor.fetchone()


def test_connection():
    result = execute_sql("SELECT VERSION()")
    if result:
        return True
    else:
        return False


# SQL queries module
# ENTITY TYPES
song = "SONG"
album = "ALBUM"
user = "USER"
comment_e = "COMME"
# ACTIVITY TYPES
follow = "FOLLO"
rate = "RATE"
share = "SHARE"
comment_a = "COMME"

'''
    Each function's inputs will be given by developers
    Herkes kendi doldurmasi gereken methodu dolduracak
    edit: tamam pasam
'''
# musab erayman
'''
    creates user,
    :return id if successful
    :return None if unsuccessful
'''


def create_user(email, name, last_name, gender, user_name, password, wallet, birth_date):
    query = """
            INSERT INTO user
            VALUES
            (DEFAULT ,%s, %s, %s, %s, %s, %s, %s, %s)
            """
    cursor = connection.cursor()
    try:
        result = cursor.execute(query, (email, name, last_name, gender, user_name, password, wallet, birth_date))
        if (result):
            connection.commit()
            result2 = cursor.lastrowid
            if (result2 != None):
                print(result2)
                return result2
            else:
                return -1
    except:
        print("The email address or username is already taken!")
        return None


'''
    checks if user with the id whether exists or not
    :return 1 if exists
    :return 0 if does not
'''


def userExists(id):
    query = """
            select exists(select * from user WHERE id = '%s')
            """ % id
    result = execute_sql(query)
    return result[0]


'''
    removes user from the user table if user with the id exists in the table
    gives error message and does not attempt to delete if the user does not exist
    ...can be expanded so that it can return true/false dependent on frontend devs' request
    ...playlist has no cascade on delete user. So I deleted manually. It should be??? We must look!!!
'''


def remove_user(id):
    if userExists(id):
        query2 = """
                  select exists(select * from playlist WHERE playlist.user_id = '%s')
                  """ % id
        hasPlaylist = execute_sql(query2)
        if hasPlaylist[0] is 1:
            execute_sql("""delete from playlist WHERE playlist.user_id = '%s'""" % id)
            print("All playlists of user with ID ", id, " are successfully deleted.")
        else:
            print("User with ID ", id, " has no playlist.")
        query = """
                delete from user WHERE id = '%s'
                """ % id
        execute_sql(query)
        print("The user with ID ", id, " is successfully deleted.")
    else:
        print("The user with ID ", id, " does not exist.")


def create_artist(email, name, last_name, gender, user_name, password, wallet, birth_date):
    id = create_user(email, name, last_name, gender, user_name, password, wallet, birth_date)
    query = """
            insert into artist
            VALUES(%s,%s) 
            """ % (id, dt.datetime.now().date())
    execute_sql(query)
    return id


def remove_artist(id):
    art_query = """
                delete from artist WHERE (artist.user_id = '%s')
                """ % (id)
    execute_sql(art_query)
    user_query = """
                 delete from user WHERE (user.id = '%s')
                 """ % (id)
    execute_sql(user_query)


'''
    :return created song id
'''


def create_song(title, release_date, duration, number_of_listen, price, album_id, artist_id, genre):
    query = """
            insert into song
            VALUES
            (DEFAULT, '%s', '%s', '%s', '%s', '%s', '%s','%s')
            """ % (title, release_date, duration, number_of_listen, price, album_id, genre)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    song_id = cursor.lastrowid
    query2 = """
                insert into artist_song
                VALUES ('%s', '%s')
                """ % (artist_id, song_id)
    execute_sql(query2)
    return song_id


def remove_song(id):
    query = """
            delete from song WHERE (song.id = '%s')
            """ % (id)
    execute_sql(query)


# ali bulut
def login_authentication(email, password):  # tested
    sql = "SELECT id FROM user WHERE (email = '%s' and password = '%s')" % (email, password)
    ret = execute_sql(sql)
    # print(ret)
    if ret != None:
        return ret[0]
    return False


def create_playlist(title, is_private, user_id):  # tested
    sql = "INSERT INTO playlist " \
          "VALUE (DEFAULT , '%s', '%s', '%s', '%s')" \
          % (title, dt.datetime.now().date(), is_private, user_id)
    execute_sql(sql)


# create_playlist("Bilkent",True,1)
def remove_playlist(playlist_id):  # tested
    sql = "DELETE FROM playlist WHERE id = '%s'" % playlist_id
    execute_sql(sql)
    return


def add_song_to_playlist(song_id, playlist_id):
    sql = "INSERT INTO playlist_song VALUE ('%s', '%s')" % (song_id, playlist_id)
    execute_sql(sql)
    return


def remove_song_from_playlist(song_id, playlist_id):
    sql = "DELETE FROM playlist_song " \
          " WHERE (song_id = '%s' AND playlist_id = '%s')" % (song_id, playlist_id)
    execute_sql(sql)
    return


def create_event(name, date, location, about):  # tested
    sql = "INSERT INTO event " \
          "VALUE (DEFAULT, '%s', '%s', '%s', '%s')" % (name, date, location, about)
    execute_sql(sql)
    return


def remove_event(id):  # tested
    sql = "DELETE FROM event WHERE id = '%s'" % id
    execute_sql(sql)
    return


def user_attend_to_event(user_id, event_id):  # tested
    sql = "INSERT INTO participation_user VALUE ('%s', '%s')" % (user_id, event_id)
    execute_sql(sql)
    return


def artist_attend_to_event(artist_id, event_id):
    sql = "INSERT INTO participation_artist VALUE ('%s', '%s')" % artist_id, event_id
    execute_sql(sql)
    return


# omer faruk karakaya
def follow_user(self_user_id, to_follow_id):
    query = """
            insert into user_follow VALUES ('%s','%s')
            """ % (self_user_id, to_follow_id)
    execute_sql(query)
    print(self_user_id, "is following user", to_follow_id)
    return


def unfollow_user():
    return


def follow_playlist():
    return


def unfollow_playlist():
    return


# kerem ayoz
def rate_song(user_id, song_id, value):
    act_id = create_activity(dt.datetime.now(), song, rate, user_id, song_id)
    print("in rate song act id = ", act_id)
    query = """
            insert into rate
            VALUES ('%s' ,'%s')
            """ % (act_id, value)
    execute_sql(query)
    print("executed")


def rate_playlist():
    return


def rate_album():
    return


def create_genre(name):
    sql = "INSERT INTO genre VALUE ('%s')" % name
    execute_sql(sql)
    return


def remove_genre(name):
    sql = "DELETE FROM genre WHERE name = '%s'" % name
    execute_sql(sql)
    return


def create_album(title, release_date, price):  # tested
    sql = "INSERT INTO album VALUE (DEFAULT, '%s', '%s', '%s')" % (title, release_date, price)
    execute_sql(sql)
    return


def remove_album(id):  # tested
    sql = "DELETE FROM album WHERE id = '%s'" % id
    execute_sql(sql)
    return


# musab erayman
def purchase_song(user_id, song_id):
    wallet = """
            select wallet from user WHERE (user.id = '%s')
            """ % (user_id)
    wallet_ = execute_sql(wallet)[0]
    song_price = """
                    select price from song WHERE (song.id = '%s')
                    """ % (song_id)
    song_price_ = execute_sql(song_price)[0]
    try:
        if song_price_ > wallet_:
            print("PMVY")
            return ("Insufficient money!")
        else:
            song_user_query = """
                              insert into user_song
                              VALUES ('%s','%s')
                              """ % (user_id, song_id)
            execute_sql(song_user_query)
            newwallet = wallet_ - song_price_
            update_query = """
                            update user set wallet = %s WHERE (user.id = '%s')
                            """ % (newwallet, user_id)
            execute_sql(update_query)
            print("Payment is done")
            return ("Payment is done")
    except pymysql.IntegrityError as e:
        if (e.args[0] == 1062):
            print("User ", user_id, " has already purchased song ", song_id)
            return ("You have already purchased this song ")


def purchase_album(user_id, album_id):
    wallet = """
            select wallet from user WHERE (user.id = '%s')
            """ % (user_id)
    wallet_ = execute_sql(wallet)[0]
    album_price = """
                    select price from album WHERE (album.id = '%s' )
                    """ % (album_id)
    album_price_ = execute_sql(album_price)[0]
    try:
        if album_price_ > wallet_:
            print("PMVY")
            return ("Insufficient money!")
        else:
            album_user_query = """
                              insert into user_album
                              VALUES ('%s','%s')
                              """ % (user_id, album_id)
            execute_sql(album_user_query)
            newwallet = wallet_ - album_price_
            update_query = """
                            update user set wallet = %s WHERE (user.id = '%s')
                            """ % (newwallet, user_id)
            execute_sql(update_query)
            print("Payment is done")
            return ("Payment is done")
    except pymysql.IntegrityError as e:
        if (e.args[0] == 1062):
            print("User ", user_id, " has already purchased album ", album_id)
            return ("You has already purchased this album ")


def add_money_to_wallet(user_id, money):
    wallet = """
            select wallet from user WHERE (user.id = '%s')
            """ % (user_id)
    wallet_ = execute_sql(wallet)
    newwallet = wallet_ + money
    update_query = """
                    update user set wallet = %s WHERE (user.id = '%s')
                    """ % (newwallet, user_id)
    execute_sql(update_query)


def create_activity(date, ent_type, act_type, user_id, entity_id):
    query = """
            insert into activity
            VALUES (DEFAULT,'%s','%s','%s','%s','%s')
            """ % (date, ent_type, act_type, user_id, entity_id)
    cursor = connection.cursor()
    cursor.execute(query)
    activity_id = cursor.lastrowid
    print(activity_id)
    return activity_id


# ali bulut
def share_song():
    return


def share_playlist():
    return


def share_album():
    return


# omer faruk karakaya
def comment_on_song():
    return


def comment_on_playlist():
    return


def comment_on_album():
    return


def comment_on_event():
    return


def reply_to_comment():
    return


def get_songs_of_users(user_id):
    sql = "SELECT song_id FROM user_song  WHERE user_id = '%s'" % user_id
    song_ids = execute_sql(sql, 1)
    res = []

    print(song_ids)

    if song_ids == None:
        return res

    for song_it in song_ids:
        sql = "SELECT * FROM song join album WHERE song.id = '%s' and song.album_id = album.id" % song_it[0]
        sng = execute_sql(sql)

        sql = """SELECT user.name FROM user WHERE user.id = 
              (SELECT artist.user_id 
              FROM artist_song natural join artist
              WHERE artist_song.song_id = '%s')""" % song_it[0]
        artist_name = execute_sql(sql)

        s = Song(sng[0], sng[1], sng[2], sng[3], sng[4], sng[5], sng[6], sng[7], artist_name[0], sng[9])
        res.append(s)

    return res


def get_songs_by_most_listened():
    sql = "SELECT song.id FROM song ORDER BY number_of_listen DESC "
    song_ids = execute_sql(sql, 1)
    res = []

    if song_ids == None:
        return res

    for song_it in song_ids:
        sql = "SELECT s.*, u.name " \
              "FROM artist a natural join artist_song a_s join song s join user u " \
              "WHERE s.id = a_s.song_id and u.id = a.user_id and a_s.song_id = '%d'" % song_it[0]
        sng = execute_sql(sql)

        s = Song(sng[0], sng[1], sng[2], sng[3], sng[4], sng[5], sng[6], sng[7], sng[8], None)
        res.append(s)

    return res


def get_albums_by_most_listened():
    sql = "SELECT album_id FROM (" \
          "SELECT sum(s.number_of_listen) ttl_nmbr, s.album_id " \
          "FROM song s " \
          "GROUP BY s.album_id) as ttl " \
          "ORDER BY ttl.ttl_nmbr DESC "
    album_ids = execute_sql(sql, 1)
    res = []

    if album_ids == None:
        return res

    for album_it in album_ids:
        sql = "SELECT a.*, u.name " \
              "FROM album a join song s on a.id = s.album_id join artist_song a_s join user u " \
              "WHERE a_s.song_id = s.id and a_s.user_id = u.id and a.id = '%s'" % album_it[0]
        albm = execute_sql(sql)

        a = Album(albm[0], albm[1], albm[2], albm[3], albm[4])
        res.append(a)

    return res


def get_songs_by_rate():
    sql = "SELECT song_id FROM song_rate "
    songs = execute_sql(sql,1)

    res = []

    if songs == None:
        return res

    for sng_it in songs:
        sql = "SELECT s.*, u.name, al.title, sr.rate  " \
              "FROM song s join artist_song a join user u join album al join song_rate sr " \
              "WHERE s.id = '%s' and a.song_id = s.id and al.id = s.album_id and a.user_id=u.id and sr.song_id = s.id" % sng_it[0]
        sng = execute_sql(sql)

        s = Song(sng[0], sng[1], sng[2], sng[3], sng[4], sng[5], sng[6], sng[7], sng[8], sng[9], sng[10])
        res.append(s)

    return res


def get_album_by_rate():
    sql = "SELECT album_id FROM album_rate"
    albums = execute_sql(sql,1)
    res = []

    if albums == None:
        return res

    for albm_it in albums:
        sql = "SELECT a.*, u.name, ar.rate " \
              "FROM album a join user u join album_rate ar join artist_song ars join song s " \
              "WHERE a.id = '%s' and a.id = ar.album_id and s.album_id = a.id and u.id = ars.user_id " % albm_it[0]
        albm = execute_sql(sql)

        a = Album( albm[0], albm[1], albm[2], albm[3], albm[4], albm[5] )
        res.append(a)

    return res


def get_followings(user_id):
    query = """select u2.* from user u1, user u2, user_follow f WHERE (u1.id = '%s' and '%s' = f.follower_id and u2.id = f.following_id)
            """ % (user_id, user_id)
    followings = execute_sql(query, 1)
    print("followers of user : ", user_id, "\n", followings)


def timeline_message(user_id):

    return


def search_user(username):
    query = "select * from user u where (u.user_name like '%" +username + "%')"
    users_tuple = execute_sql(query,1)
    users = []

    for i in range(len(users_tuple)) :
        users.append(User(user_id= users_tuple[i][0], username= users_tuple[i][5]))
    return users


def search_song(songtitle):
    query = "select * from song s where (s.title like '%" +songtitle + "%')"
    songs_tuple = execute_sql(query,1)
    songs = []
    for i in range(len(songs_tuple)) :
        songs.append(Song(song_id= songs_tuple[i][0], title= songs_tuple[i][1], price=songs_tuple[i][5],
                     genre= songs_tuple[i][7]))
    print(songs_tuple)
    return songs


def search_album(albumtitle):
    query = "select * from album a where (a.title like '%" +albumtitle + "%')"
    albums_tuple = execute_sql(query,1)
    albums = []
    for i in range(len(albums_tuple)) :
        albums.append(Album(album_id= songs_tuple[i][0], title= songs_tuple[i][1], price=songs_tuple[i][3]))
    return albums


def search_playlist(playlisttitle):
    query = "select * from playlist p where p.title like '%" +playlisttitle + "%' and p.is_private = False"
    playlists_tuple = execute_sql(query,1)
    playlists = []
    for i in range(len(playlists_tuple)) :
        playlists.append(Playlist(playlist_id= playlists_tuple[i][0], title= playlists_tuple[i][1]))
    return playlists


def search_events(eventtitle):
    query = "select * from event e where e.title like '%" + eventtitle + "%'"
    events_tuple = execute_sql(query,1)
    events = []
    for i in range(len(events_tuple)) :
        events.append(Event(event_id= events_tuple[i][0], name= events_tuple[i][1], date=events_tuple[i][2],
                            location=events_tuple[i][3], about=events_tuple[i][4]))
    return events

# create_user('basi3','isim','soyisim','male','piley23',"password",'3',dt.datetime(2000,2,3))
# remove_user(1)

# converts seconds to min and sec
# time.strftime( "%M:%S", time.gmtime(186) )

# create_album("Use Your Illusion", dt.datetime(1991,1,1), 20)
# create_song("Dont Cry", dt.datetime(1991,1,1), time.strftime("%M%S",time.gmtime(284)), 3, 5, 2)
# create_artist('esda@dasadsda','isim','ast','male','ushsarkierer',"pass",'3',dt.datetime(2000,2,1))
# create_song("title",dt.datetime(1995,12,1),time.strftime("%M%S",time.gmtime(284)),1,3,2,105,'rock')
# rate_song(108,4,5)
#purchase_album(86, 2)
search_song("cry")
