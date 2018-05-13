class User:

    def __init__(self, user_id = None, name = None, lastname = None, username = None, birth_date = None, wallet = None, email = None):
        self.user_id = user_id
        self.name = name
        self.lastname = lastname
        self.username = username
        self.birth_date = birth_date
        self.wallet = wallet
        self.email = email


class Artist:

    def __init__(self, user_id, name, lastname, gender, birth_date, wallet, account_validation_date):
        User.__init__(user_id, name, lastname, gender, birth_date, wallet)
        self.account_validation_date = account_validation_date


# Genre is a separate table in db but added into a Song in class diagram because it has no other function
class Song:

    def __init__(self, song_id = None, title = None, release_date =None, duration =None,
                 number_of_listen =None, price =None, album_id = None, genre =None,
                 artist_name =None, album_name =None, rate=None):
        self.song_id = song_id
        self.title = title
        self.release_date = release_date
        self.duration = duration
        self.number_of_listen = number_of_listen
        self.price = price
        self.album_id = album_id
        self.genre = genre
        self.artist_name = artist_name
        self.album_name = album_name
        self.rate = rate


class Playlist:

    def __init__(self, playlist_id=None, title=None, create_date=None, is_private=None):
        self.playlist_id = playlist_id
        self.title = title
        self.create = create_date
        self.is_private = is_private


class Album:

    def __init__(self, album_id=None, title=None, release_date=None, price=None, artist=None, rate=None):
        self.album_id = album_id
        self.title = title
        self.release_date = release_date
        self.price = price
        self.artist = artist
        self.rate = rate


class Event:

    def __init__(self, event_id=None, name=None, date=None, location=None, about=None):
        self.event_id = event_id
        self.name = name
        self.date = date
        self.location = location
        self.about = about


class Activity:

    def __init__(self, activity_id, date, entity_type, action_type):
        self.activity_id = activity_id
        self.date = date
        self.entity_type = entity_type
        self.action_type = action_type


class Share:

    def __init__(self, activity_id, date, entity_type, action_type, share_comment):
        Activity.__init__(activity_id, date, entity_type, action_type)
        self.share_comment = share_comment


class Rate:
    def __init__(self, activity_id, date, entity_type, action_type, rate):
        Activity.__init__(activity_id, date, entity_type, action_type)
        self.rate = rate


class Comment:
    def __init__(self, activity_id, date, entity_type, action_type, text, parent_id, reply_list):
        Activity.__init__(activity_id, date, entity_type, action_type)
        self.text = text
        self.parent_id = parent_id
        self.reply_list = reply_list


class ActivityReport:
    def __init__(self, activity_id, date, entity_type, entity_id, text):
        self.activity_id = activity_id
        self.date = date
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.text = text
