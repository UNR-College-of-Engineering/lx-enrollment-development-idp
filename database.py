import sqlite3

conn = sqlite3.connect('database.db')
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (sub CHAR[21],username VARCHAR[255])""")
conn.commit()

def insertUser(sub, username):
    if checkUser(sub, username):
        return False
    c.execute("""insert into users values (?,?)""",(sub,username))
    conn.commit()
    print("User added")
    return True

def checkUser(sub, username):
    all = c.execute("""select * from users""").fetchall()
    for entry in all:
        if sub in entry and username in entry:
            print("User already exists")
            return True
    return False

def printUsers():
    all = c.execute("""select * from users""").fetchall()
    print(all)