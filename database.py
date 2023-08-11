import sqlite3

conn = sqlite3.connect('database.db')
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (preffered_username VARCHAR[255],chosenclass VARCHAR[255])""")
conn.commit()

def insertUser(username, classname):
    if checkUser(username):
        return False
    c.execute("""insert into users values (?,?)""",(username, classname))
    conn.commit()
    print("User added")
    return True

def checkUser(username):
    all = c.execute("""select * from users""").fetchall()
    for entry in all:
        if username in entry:
            print("User already exists")
            return True
    return False

def printUsers():
    all = c.execute("""select * from users""").fetchall()
    print(all)