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
    :return Node if unsuccessful
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

def remove_user():
    return
def create_artist():
    return
def remove_artist():
    return
def create_song():
    return
def remove_song():
    return
# ali bulut
def login_authentication(email, password):
    sql = "SELECT id FROM user WHERE (email = '%s' and password = '%s')" % (email, password)
    ret = execute_sql(sql)
    #print(ret)
    if ret != None:
        return ret[0]
    return False

def create_playlist( title, is_private, user_id):
    sql = "INSERT INTO playlist " \
          "VALUE (DEFAULT , '%s', '%s', '%s', '%s')" \
          % (title, dt.datetime.now().date(), is_private, user_id)
    execute_sql(sql)

create_playlist("Bilkent",True,1)

def remove_playlist():
    return
def add_song_to_playlist():
    return
def remove_song_from_playlist():
    return
def create_event():
    return
def remove_event():
    return
def attend_to_event():
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
def rate_song():
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
def purchase_song():
    return
def purchase_album():
    return
def add_money_to_wallet():
    return
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
create_user('basi3','isim','soyisim','male','piley23',"password",'3',dt.datetime(2000,2,3))