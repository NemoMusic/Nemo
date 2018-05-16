import pymysql
import datetime as dt
import time



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
event = "EVENT"
playlist = "PLIST"
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


def get_User(id):
    query="select * from user where id = '%id'"%id
    user = execute_sql(query);
    print(user)
    return User(user_id=user[0],username=user[5],name=user[2],lastname=user[3],wallet=user[7])
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
    sql = "SELECT * FROM participation_user WHERE user_id = '%s' and event_id = '%s'" \
          % (user_id, event_id)
    ret = execute_sql(sql)
    if ret != None:
        return "You Already Participated This Event!"

    sql = "INSERT INTO participation_user VALUE ('%s', '%s')" % (user_id, event_id)
    execute_sql(sql)
    return "You Successfully Participated This Event!"


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


def unfollow_user(self_user_id, to_unfollow_id):
    query = """
            delete from user_follow WHERE (user_follow.follower_id = '%s' AND user_follow.following_id = '%s')
            """ % (self_user_id,to_unfollow_id)
    execute_sql(query)
    return


def follow_playlist(self_user_id, playlist_id):
    query = """
            insert into activity VALUES (DEFAULT, '%s','%s', '%s', '%s', '%s')
            """ % (dt.datetime.now().date(), playlist, follow, self_user_id, playlist_id)
    execute_sql(query)
    return


def unfollow_playlist(activity_id):
    query = """
            delete from activity WHERE id = '%s'
            """ % activity_id
    execute_sql(query)
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


def rate_playlist(user_id, playlist_id, value):
    act_id = create_activity(dt.datetime.now(), playlist, rate, user_id, playlist_id)
    print("in rate playlist act id = ", act_id)
    query = """
            insert into rate
            VALUES ('%s' ,'%s')
            """ % (act_id, value)
    execute_sql(query)
    print("executed")


def rate_album(user_id, album_id,value):
    act_id = create_activity(dt.datetime.now(), playlist, rate, user_id, album_id)
    print("in rate album act id = ", act_id)
    query = """
            insert into rate
            VALUES ('%s' ,'%s')
            """ % (act_id, value)
    execute_sql(query)
    print("executed")
#def create_genre(name):
#   sql = "INSERT INTO genre VALUE ('%s')" % name
#   execute_sql(sql)
#   return


#def remove_genre(name):
#   sql = "DELETE FROM genre WHERE name = '%s'" % name
#    execute_sql(sql)
#    return


def create_album(title, release_date, price):  # tested
    sql = "INSERT INTO album VALUE (DEFAULT, '%s', '%s', '%s')" % (title, release_date, price)
    execute_sql(sql)
    return


def remove_album(id):  # tested
    sql = "DELETE FROM album WHERE id = '%s'" % id
    execute_sql(sql)
    return


def delete_user_song(user_id, song_id):
    sql = "DELETE FROM user_song WHERE user_id = '%s' and song_id = '%s'" % (user_id, song_id)
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
def share_song(user_id, entity_id, share_comment):
    sql = "INSERT INTO activity VALUE (DEFAULT '%s', '%s', '%s', '%s', '%s' )" \
          % (dt.datetime.now().date(), song, share, user_id, entity_id)
    execute_sql(sql)
    id = connection.cursor().lastrowid
    sql = "INSERT INTO share VALUE ('%s', '%s')" % (id, share_comment)
    execute_sql(sql)
    return


def share_playlist(user_id, entity_id, share_comment):
    sql = "INSERT INTO activity VALUE (DEFAULT '%s', '%s', '%s', '%s', '%s' )" \
          % (dt.datetime.now().date(), playlist, share, user_id, entity_id)
    execute_sql(sql)
    id = connection.cursor().lastrowid
    sql = "INSERT INTO share VALUE ('%s', '%s')" % (id, share_comment)
    execute_sql(sql)
    return


def share_album(user_id, entity_id, share_comment):
    sql = "INSERT INTO activity VALUE (DEFAULT '%s', '%s', '%s', '%s', '%s' )" \
          % (dt.datetime.now().date(), album, share, user_id, entity_id)
    execute_sql(sql)
    id = connection.cursor().lastrowid
    sql = "INSERT INTO share VALUE ('%s', '%s')" % (id, share_comment)
    execute_sql(sql)
    return


# omer faruk karakaya
def comment_on_song( user_id, song_id, comment_text ):
    sql = "INSERT INTO activity VALUE (DEFAULT, '%s', '%s', '%s', '%s', '%s')" \
          % (dt.datetime.now().date(), comment_e, song, user_id, song_id)
    execute_sql(sql)
    id = connection.cursor().lastrowid
    sql = "INSERT INTO comment VALUE ('%s', '%s')" % (id, comment_text)
    execute_sql(sql)
    return


def comment_on_playlist( user_id, song_id, comment_text ):
    sql = "INSERT INTO activity VALUE (DEFAULT, '%s', '%s', '%s', '%s', '%s')" \
          % (dt.datetime.now().date(), playlist, comment_a, user_id, song_id)
    execute_sql(sql)
    id = connection.cursor().lastrowid
    sql = "INSERT INTO comment VALUE ('%s', '%s')" % (id, comment_text)
    execute_sql(sql)
    return


def comment_on_album( user_id, song_id, comment_text ):
    sql = "INSERT INTO activity VALUE (DEFAULT, '%s', '%s', '%s', '%s', '%s')" \
          % (dt.datetime.now().date(), album, comment_a, user_id, song_id)
    execute_sql(sql)
    id = connection.cursor().lastrowid
    sql = "INSERT INTO comment VALUE ('%s', '%s')" % (id, comment_text)
    execute_sql(sql)
    return


def comment_on_event( user_id, song_id, comment_text ):
    sql = "INSERT INTO activity VALUE (DEFAULT, '%s', '%s', '%s', '%s', '%s')" \
          % (dt.datetime.now().date(), event,  comment_a, user_id, song_id)
    execute_sql(sql)
    id = connection.cursor().lastrowid
    sql = "INSERT INTO comment VALUE ('%s', '%s')" % (id, comment_text)
    execute_sql(sql)
    return


def reply_to_comment( user_id, song_id, comment_text ):
    sql = "INSERT INTO activity VALUE (DEFAULT, '%s', '%s', '%s', '%s', '%s')" \
          % (dt.datetime.now().date(), comment_e, comment_a, user_id, song_id)
    execute_sql(sql)
    id = connection.cursor().lastrowid
    sql = "INSERT INTO comment VALUE ('%s', '%s')" % (id, comment_text)
    execute_sql(sql)
    return


def get_songs_of_users(user_id):
    sql = "SELECT song_id FROM user_song  WHERE user_id = '%s'" % user_id
    song_ids = execute_sql(sql, 1)
    res = []
    sql = "SELECT s.id " \
          "FROM user_album ua join song s on s.album_id = ua.album_id " \
          "WHERE ua.user_id = '%s'" % user_id
    song_ids += execute_sql(sql, 1)
    song_ids = set(song_ids)

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
    sql = "SELECT song_id FROM song_rate ORDER BY rate DESC"
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
    sql = "SELECT album_id FROM album_rate ORDER BY rate DESC"
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
    query = """select following.user_name from user following, user_follow f WHERE ('%s' = f.follower_id and following.id = f.following_id)
            """ % (user_id)
    followings = execute_sql(query, 1)
    print("followings of user : ", user_id, "\n")
    followinglist = []
    for i in range(len(followings)):
        followinglist.append(followings[i][0])
        print(followinglist[i])
    return followinglist


def get_followers(user_id):
    query = """select follower.user_name from user follower, user_follow f WHERE ('%s' = f.following_id and follower.id = f.follower_id)
            """ % (user_id)
    followers = execute_sql(query, 1)
    print("followers of user : ", user_id, "\n")
    followerlist = []
    for i in range(len(followers)):
        followerlist.append(followers[i][0])
        print(followerlist[i])
    return followerlist


def timeline_message(user_id):
    query = """
            select  following.user_name, a.date, a.entity_type, a.entity_id, a.action_type,
            case a.action_type
              WHEN '%s' THEN '%s'
              WHEN '%s' THEN share.share_comment
              WHEN '%s' THEN comment.text
              WHEN '%s' THEN rate.value
            END
            FROM user following JOIN user_follow uf JOIN activity a
            LEFT OUTER JOIN follow ON (a.id = follow.activity_id)
            LEFT OUTER JOIN rate on (a.id = rate.activity_id) 
            LEFT OUTER JOIN share ON (a.id = share.activity_id)
            LEFT OUTER JOIN comment ON (a.id = comment.activity_id)
            WHERE ('%s' = uf.follower_id and following.id = uf.following_id and a.user_id = following.id) 
            """ %(follow,user_id,share,comment_a,rate,user_id)
    message = execute_sql(query,1)

    logarray = []
    for i in range(len(message)):
        username = message[i][0]
        date = message[i][1]
        entitytype = message[i][2]
        entity_id = message[i][3]
        act_type = message[i][4]
        act_content = message[i][5]
        #it will return html
        if act_content != None:
            if act_type == rate:
                if entitytype == song:
                    sql = "SELECT title FROM song WHERE id = '%s'" % entity_id
                else:
                    sql = "SELECT title FROM album WHERE id = '%s'" % entity_id
                rated_item = execute_sql(sql)
                rated_item = rated_item[0]
                log = '<a href="http://link">'+ username +'</a><p style="text-align: right;"> has rated </p><a href="/user?username='+ username +'">'+ rated_item + ' as ' + act_content + ' star</a>'
                logarray.append(log)
            elif act_type == follow:
                sql = "SELECT name FROM user WHERE id = '%s'" % entity_id
                username2 = execute_sql(sql)
                username2 = username2[0]
                log = '<a href="http://link">' + username + '</a><p style="text-align: right;"> has followed </p><a href="/user?username=' + username2 + '">' + username2 + '</a>'
                logarray.append(log)
            elif act_type == share:
                if entitytype == song:
                    sql = "SELECT title FROM song WHERE id = '%s'" % entity_id
                elif entitytype == album:
                    sql = "SELECT title FROM album WHERE id = '%s'" % entity_id
                else:
                    sql = "SELECT title FROM playlist WHERE id = '%s'" % entity_id
                shared_item = execute_sql(sql)
                shared_item = shared_item[0]
                log = '<a href="http://link">' + username + '</a><p style="text-align: right;"> has shared </p><a href="/user?username=' + shared_item + '"></a>'
                logarray.append(log)
            elif act_type == comment_a:
                sql = "SELECT text FROM comment WHERE activity_id = '%s'" % entity_id
                comment = execute_sql(sql)
                comment = comment[0]
                log = '<a href="http://link">' + username + '</a><p style="text-align: right;"> shared comment: </p><a href="/user?username=' + comment + '"></a>'
                logarray.append(log)
    for k in range(len(logarray)):
        print(logarray[k])
    return logarray


def get_attended_events(user_id):
    sql = "SELECT event_id FROM participation_user WHERE user_id = '%s'" % user_id
    attended_events = execute_sql(sql, 1)

    res = []

    if attended_events == None:
        return res

    for event_it in attended_events:
        sql = "SELECT * FROM event WHERE id = '%s'" % event_it[0]
        ret = execute_sql(sql)
        e = Event(ret[0], ret[1], ret[2], ret[3], ret[4])
        res.append(e)

    return res


def get_all_events():
    sql = "SELECT id FROM event"
    event_ids = execute_sql(sql,1)
    res = []

    for it in event_ids:
        sql = "SELECT * FROM event WHERE id = '%s'" % it[0]
        ret = execute_sql(sql)
        print(ret[0], ret[1], ret[2], ret[3], ret[4])
        e = Event(ret[0], ret[1], ret[2], ret[3], ret[4])
        res.append(e)

    return res


def get_songs_of_playlist(playlist_id):
    sql = "SELECT song_id FROM playlist_song WHERE playlist_id = '%s'" % playlist_id
    playlist_songs = execute_sql(sql,1)

    res = []
    if playlist_songs == None:
        return res

    for sng_it in playlist_songs:
        sql = "SELECT s.*, u.name, al.title, sr.rate  " \
              "FROM song s join artist_song a join user u join album al join song_rate sr " \
              "WHERE s.id = '%s' and a.song_id = s.id and al.id = s.album_id and a.user_id=u.id and sr.song_id = s.id" % \
              sng_it[0]
        sng = execute_sql(sql)

        s = Song(sng[0], sng[1], sng[2], sng[3], sng[4], sng[5], sng[6], sng[7], sng[8], sng[9], sng[10])
        res.append(s)

    return res


def get_comments_of_playlist(playlist_id):
    sql = "SELECT id FROM activity WHERE entity_type = '%s' and action_type = '%s' and entity_id = '%s' " \
        % (playlist, comment_a, playlist_id)
    comments_playlist = execute_sql(sql,1)

    res = []

    if comments_playlist == None:
        return res

    for act_id in comments_playlist:
        sql = "SELECT a.id, a.date, a.entity_type, a.action_type, c.text  " \
              "FROM activity a join comment c on (c.activity_id = a.id) " \
              "WHERE a.id = '%s'" % act_id[0]
        ret = execute_sql(sql)
        c = Comment(ret[0], ret[1], ret[2], ret[3], ret[4], None, None)
        res.append(c)

    return res


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
        albums.append(Album(album_id= albums_tuple[i][0], title= albums_tuple[i][1], price= albums_tuple[i][3]))
    return albums


def search_playlist(playlisttitle):
    query = "select * from playlist p where p.title like '%" +playlisttitle + "%' and p.is_private = False"
    playlists_tuple = execute_sql(query,1)
    playlists = []
    for i in range(len(playlists_tuple)) :
        playlists.append(Playlist(playlist_id= playlists_tuple[i][0], title= playlists_tuple[i][1]))
    return playlists


def search_events(eventtitle):
    query = "select * from event e where e.name like '%" + eventtitle + "%'"
    events_tuple = execute_sql(query,1)
    events = []
    for i in range(len(events_tuple)) :
        events.append(Event(event_id= events_tuple[i][0], name= events_tuple[i][1], date=events_tuple[i][2],
                            location=events_tuple[i][3], about=events_tuple[i][4]))
    return events


def levenshtein_distance(x,y):
    if not len(x):
        return len(y)
    if not len(y):
        return len(x)
    return min(levenshtein_distance(x[1:], y[1:]) + (x[0] != y[0]), levenshtein_distance(x[1:], y) + 1, levenshtein_distance(x, y[1:]) + 1)


def did_u_mean_user(searchq,treshold):
    user_query = """
            select user.user_name from user
            """
    others = execute_sql(user_query,1)
    for i in range(len(others)):
        if(levenshtein_distance(searchq,others[i][5])<treshold):
            print("Did you mean " + others[i][5])
            return "Did you mean " + others[i][5]


def get_users_playlists(userid):
    playlists = []
    query = """
            select p.id, p.title from playlist p WHERE (p.user_id = '%s')
            """ % (userid)
    plists = execute_sql(query, 1)
    for it in plists:
        pl = Playlist(it[0], it[1], None, None)
        playlists.append(pl)
    return playlists


def get_following_playlist(userid):
    playlists = []
    query = """
          SELECT a.entity_id
          FROM activity a join user u on (a.user_id = u.id) 
          WHERE a.action_type = '%s' and a.entity_type = '%s' and u.id = '%s'
            """ % (follow, playlist, userid)
    plists = execute_sql(query, 1)
    for it in plists:
        sql = "SELECT * FROM playlist p WHERE p.id = '%s'" % it[0]
        ret = execute_sql(sql)
        pl = Playlist(ret[0], ret[1], ret[2], ret[3])
        playlists.append(pl)

    return playlists


def get_userid_by_username(username):
    sql = "SELECT id FROM user WHERE user_name = '%s'" % username
    u = execute_sql(sql)
    print(u[0])
    return u[0]

def optimizeUser():
    query = """
              UPDATE user 
              SET email = 'dba@lookman.com', name = 'Kerem', last_name = 'Ayöz', user_name = 'kerem_ayoz', password = '123', wallet = 1905  
              WHERE id = 10
                """
    execute_sql(query)
    return

#create_user('basi3','isim','soyisim','male','piley23',"password",'3',dt.datetime(2000,2,3))
# remove_user(1)

# converts seconds to min and sec
# time.strftime( "%M:%S", time.gmtime(186) )

# create_album("Use Your Illusion", dt.datetime(1991,1,1), 20)
# create_song("Dont Cry", dt.datetime(1991,1,1), time.strftime("%M%S",time.gmtime(284)), 3, 5, 2)
# create_artist('esda@dasadsda','isim','ast','male','ushsarkierer',"pass",'3',dt.datetime(2000,2,1))
# create_song("title",dt.datetime(1995,12,1),time.strftime("%M%S",time.gmtime(284)),1,3,2,105,'rock')
# rate_song(108,4,5)
# purchase_album(86, 2)
# search_song("cry")
#timeline_message(10)
# print(levenshtein_distance("blknt", "bilkent"))
# get_followings(104)
# get_following_playlist(10)
# optimizeUser()

