import random
from datetime import datetime
import string

uppercaseletters = string.ascii_uppercase
lowercaseletters = string.ascii_lowercase
specialcharacters = "!@#$%^&*()_-+="
numerics = string.digits

#user data variables
user_id = 1
names = ("Ahmet","Arif","Omer","Kerem","Ercument","Ali", "Musab","Emma","Oznur","Ayse","Cagri", "Rachel", "Deniz","Karl","Sophie","Anna","Jennifer","Sila","Mike","Feyza")
emails = set
lastnames = ("Sahin","Yildiz","Cicek","Erayman","Karakaya","Corey","Bulut","Usta","Ayoz","Toraman","Sneijder","Roosvelt","Thompson","Trump","Alkan","Sawyer")
genders = ("Male","Female","Not to disclose")
usernames = set
passwords = []
wallets = []
birthdate = []
#genre data variables
#song data variables

def userGenerate(number):
    for x in range(number):
        name = random.choice(names)
        lastname = random.choice(lastnames)
        gender = random.choice(genders)
        usernamelen = random.choice(range(0,15))
        username = random.choice(lowercaseletters) + random.choice(uppercaseletters) + random.choice(specialcharacters) + random.choice(numerics)
        for a in range(usernamelen):
            case = random.randint(1,4)
            if case == 1:
                username += random.choice(lowercaseletters)
            elif case == 2:
                username += random.choice(uppercaseletters)
            elif case == 3:
                username += random.choice(specialcharacters)
            else:
                username += random.choice(numerics)
        wallet = random.uniform(0.0,1000.0)
        print("",user_id ,"username = ", username , "",name , "",lastname , "",gender , "",wallet)

def artistGenerate(number):
    return
def genreGenerate(number):
    return
def songGenerate(number):
    return
def birthdateGenerate(number):
    for x in range(number):
        year = random.choice(range(1940, 2010))
        month = random.choice(range(1, 13))
        day = random.choice(range(1, 29))
        birthdate.append(datetime(year, month, day))
birthdateGenerate(100)
userGenerate(100)

'''
for bd in birthdate:
    print(bd)
'''