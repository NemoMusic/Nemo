class User:

    def __init__(self, user_id, name, lastname, gender, birth_date, wallet):
        self.user_id = user_id
        self.name = name
        self.lastname = lastname
        self.gender = gender
        self.birth_date = birth_date
        self.wallet = wallet


class Artist:

    def __init__(self, user_id, name, lastname, gender, birth_date, wallet, account_validation_date):
        User.__init__(user_id, name, lastname, gender, birth_date, wallet)
        self.account_validation_date = account_validation_date


# Genre is a seperate table in db but added into a Song in class diagram because it has no other function
class Song:

    def __init__(self, user_id, title, release_date, duration, number_of_listen, price, album_id, genres):
        self.user_id = user_id
        self.title = title
        self.release_date = release_date
        self.duration = duration
        self.number_of_listen = number_of_listen
        self.price = price
        self.album_id = album_id
        self.genres = genres


class Playlist:

    def __init__(self, playlist_id, title, create_date, is_private):
        self.playlist_id = playlist_id
        self.title = title
        self.create = create_date
        self.is_private = is_private


class Album:

    def __init__(self, album_id, title, release_date, price):
        self.album_id = album_id
        self.title = title
        self.release_date = release_date
        self.price = price


class Event:

    def __init__(self, event_id, name, date, location, about):
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
        Activity.__init__(activity_id ,date, entity_type, action_type)
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





