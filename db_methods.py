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
    edit: tamam paşam
'''
# musab erayman
def create_user(id,email,name,last_name,gender,user_name,password,wallet,birth_date):
    query = """
            INSERT INTO user
            VALUES
            (%s,%s, %s, %s, %s, %s, %s, %s, %s)
            """
    cursor = connection.cursor()
    cursor.execute(query, (id, email, name, last_name, gender, user_name, password, wallet,None))
    connection.commit()
    return cursor.fetchone()

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


def create_playlist():
    return
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
#create_user(2,'sa@gamail.com','isim','soyisim','male','player',"password",'3',None)