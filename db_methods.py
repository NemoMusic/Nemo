import pprint
import pymysql
import datetime as dt
import time
connection = None

connection = pymysql.connect(host='nemo.cnj8noexhne9.eu-west-1.rds.amazonaws.com',
                            user='nemo',
                            password='nemoadmin',
                            db='nemodb')

def execute_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchone()

def test_connection():
    result = execute_sql("SELECT VERSION()")
    if result:
        return True
    else:
        return False
#SQL queries module
from db_manager import execute_sql

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
def create_user(email,name,last_name,gender,user_name,password,wallet,birth_date):
    query = """
            INSERT INTO user
            VALUES
            (DEFAULT ,%s, %s, %s, %s, %s, %s, %s, %s)
            """
    cursor = connection.cursor()
    try:
        result = cursor.execute(query, (email, name, last_name, gender, user_name, password, wallet,birth_date))
        if(result):
            connection.commit()
            result2 = cursor.lastrowid
            if(result2 != None):
                print(result2)
                return result2
            else:
                return None
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

def create_artist(email,name,last_name,gender,user_name,password,wallet,birth_date):
    id = create_user(email,name,last_name,gender,user_name,password,wallet,birth_date)
    query = """
            insert into artist
            VALUES(%s,%s) 
            """ %(id,dt.datetime.now().date())
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
def create_song(title,release_date,duration,number_of_listen,price,album_id):
    query = """
            insert into song
            VALUES
            (DEFAULT, '%s', '%s', '%s', '%s', '%s', '%s', )
            """ %(title,release_date,duration,number_of_listen,price,album_id)
    execute_sql(query)
def remove_song(id):
    query = """
            delete from song WHERE (song.id = '%s')
            """ % (id)
    execute_sql(query)
# ali bulut
def login_authentication(email, password): #tested
    sql = "SELECT id FROM user WHERE (email = '%s' and password = '%s')" % (email, password)
    ret = execute_sql(sql)
    #print(ret)
    if ret != None:
        return ret[0]
    return False
def create_playlist( title, is_private, user_id): #tested
    sql = "INSERT INTO playlist " \
          "VALUE (DEFAULT , '%s', '%s', '%s', '%s')" \
          % (title, dt.datetime.now().date(), is_private, user_id)
    execute_sql(sql)
#create_playlist("Bilkent",True,1)
def remove_playlist( playlist_id ): #tested
    sql = "DELETE FROM playlist WHERE id = '%s'" % playlist_id
    execute_sql(sql)
    return
def add_song_to_playlist( song_id, playlist_id):
    sql = "INSERT INTO playlist_song VALUE ('%s', '%s')" % (song_id, playlist_id)
    execute_sql(sql)
    return
def remove_song_from_playlist( song_id, playlist_id):
    sql = "DELETE FROM playlist_song " \
          " WHERE (song_id = '%s' AND playlist_id = '%s')" % (song_id, playlist_id)
    execute_sql(sql)
    return
def create_event( name, date, location, about): #tested
    sql = "INSERT INTO event " \
          "VALUE (DEFAULT, '%s', '%s', '%s', '%s')" % (name, date, location, about)
    execute_sql(sql)
    return
def remove_event( id ): #tested
    sql = "DELETE FROM event WHERE id = '%s'" % id
    execute_sql(sql)
    return
def user_attend_to_event( user_id, event_id ): #tested
    sql = "INSERT INTO participation_user VALUE ('%s', '%s')" % (user_id, event_id)
    execute_sql(sql)
    return
def artist_attend_to_event( artist_id, event_id ):
    sql = "INSERT INTO participation_artist VALUE ('%s', '%s')" % artist_id, event_id
    execute_sql(sql)
    return
# omer faruk karakaya
def follow_user():
    return
def unfollow_user():
    return
def follow_playlist():
    return
def unfollow_playlist():
    return
# kerem ayoz
def rate_song(song_id):
    return
def rate_playlist():
    return
def rate_album():
    return
def create_genre():
    return
def remove_genre():
    return
def create_album():
    return
def remove_album():
    return
# musab erayman
def purchase_song(user_id,song_id):
    wallet ="""
            select wallet from user WHERE (user.id = '%s')
            """ % (user_id)
    wallet_ = execute_sql(wallet)
    song_price =    """
                    select price from song WHERE (song.id = '%s' )
                    """ % (song_id)
    song_price_ = execute_sql(song_price)
    if song_price_ > wallet_:
        print("PMVY")
        return None
    else:
        newwallet = wallet_ - song_price_
        update_query =  """
                        update user set wallet = %s WHERE (user.id = '%s')
                        """ %(newwallet,user_id)
        execute_sql(update_query)
def purchase_album(user_id,album_id):
    wallet ="""
            select wallet from user WHERE (user.id = '%s')
            """ % (user_id)
    wallet_ = execute_sql(wallet)
    album_price =    """
                    select price from album WHERE (album.id = '%s' )
                    """ % (album_id)
    album_price_ = execute_sql(album_price)
    if album_price_ > wallet_:
        print("PMVY")
        return None
    else:
        newwallet = wallet_ - album_price_
        update_query =  """
                        update user set wallet = %s WHERE (user.id = '%s')
                        """ %(newwallet,user_id)
        execute_sql(update_query)
def add_money_to_wallet(user_id,money):
    wallet ="""
            select wallet from user WHERE (user.id = '%s')
            """ % (user_id)
    wallet_ = execute_sql(wallet)
    newwallet = wallet_ + money
    update_query =  """
                    update user set wallet = %s WHERE (user.id = '%s')
                    """ %(newwallet,user_id)
    execute_sql(update_query)
def create_activity(date,ent_type,act_type,user_id):
    query = """
            insert into activity
            VALUES (DEFAULT,'%s','%s','%s','%s')
            """ % (date,ent_type,act_type,user_id)
    execute_sql(query)
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
#create_user('basi3','isim','soyisim','male','piley23',"password",'3',dt.datetime(2000,2,3))
#remove_user(1)