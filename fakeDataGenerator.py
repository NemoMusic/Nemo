import random
from db_methods import create_user
from datetime import date
import string

uppercaseletters = string.ascii_uppercase
lowercaseletters = string.ascii_lowercase
specialcharacters = "!@#$%^&*()_-+="
numerics = string.digits

# user data variables
user_id = 1
names = (
"Ahmet", "Arif", "Omer", "Kerem", "Ercument", "Ali", "Musab", "Emma", "Oznur", "Ayse", "Cagri", "Rachel", "Deniz",
"Karl", "Sophie", "Anna", "Jennifer", "Sila", "Mike", "Feyza")
emails = set
lastnames = (
"Sahin", "Yildiz", "Cicek", "Erayman", "Karakaya", "Corey", "Bulut", "Usta", "Ayoz", "Toraman", "Sneijder", "Roosvelt",
"Thompson", "Trump", "Alkan", "Sawyer")
genders = ("Male", "Female", "Not to disclose")
usernames = set
passwords = []
wallets = []
birthdate = []


# genre data variables
# song data variables
def birthdateGenerate():
    year = random.choice(range(1940, 2010))
    month = random.choice(range(1, 13))
    day = random.choice(range(1, 29))
    birthdate = date(year, month, day)
    return birthdate


def userGenerate(number):
    for x in range(number):
        name = random.choice(names)
        lastname = random.choice(lastnames)
        gender = random.choice(genders)
        usernamelen = random.choice(range(0, 15))
        username = random.choice(lowercaseletters) + random.choice(uppercaseletters) + random.choice(
            specialcharacters) + random.choice(numerics)
        password = random.choice(lowercaseletters) + random.choice(uppercaseletters) + random.choice(
            specialcharacters) + random.choice(numerics)
        for a in range(usernamelen):
            case = random.randint(1, 4)
            if case == 1:
                username += random.choice(lowercaseletters)
                password += random.choice(lowercaseletters)
            elif case == 2:
                username += random.choice(uppercaseletters)
                password += random.choice(uppercaseletters)
            elif case == 3:
                username += random.choice(specialcharacters)
                password += random.choice(specialcharacters)
            else:
                username += random.choice(numerics)
        wallet = random.uniform(0.0, 1000.0)
        birthdate = birthdateGenerate()
        email = "" + username + "." + name + "@gmail.com"
        create_user(email, name, lastname, gender, username, password, wallet, birthdate)


def artistGenerate(number):
    return


def genreGenerate(number):
    return


def songGenerate(number):
    return


userGenerate(10)

'''
for bd in birthdate:
    print(bd)
'''
