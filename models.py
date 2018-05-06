class User:

    def __init__(self,id,name,lastname,gender,birth_date,wallet):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.gender = gender
        self.birth_date = birth_date
        self.wallet = wallet


class Song:

    def __init__(self,id,title,release_date,duration,number_of_listen,price):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.duration = duration
        self.number_of_listen = number_of_listen
        self.price = price
