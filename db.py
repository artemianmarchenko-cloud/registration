import sqlite3

DB_NAME = "reg.db"


def create_conection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    avatar TEXT NOT NULL,)''')
    conn.commit()

def addField():
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''
    ALTER TABLE users ADD COLUMN avatar TEXT''')
    conn.commit()

def reg_user(username, password):
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (username, password) VALUES (?, ?)''',
                   (username, password))
    conn.commit()

def get_user(username):
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE username = ?''', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def edit_user(newusername, newpassword, username, avatar):
    conn = create_conection()
    cursor = conn.cursor()
    if avatar != "None":
        print("if")
        cursor.execute('''
        UPDATE users SET username = ?, password = ?,
        avatar = ? WHERE username = ?''',
                       (newusername, newpassword, avatar, username))
        conn.commit()

    else:
        print("else")
        cursor.execute('''
               UPDATE user SET username = ?, password = ?,
               WHERE username = ?''',
                       (newusername, newpassword, username))
        conn.commit()

    conn.close()

def createMessages():
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    conn.commit()
    conn.close()

def saveMessages(user_id, text):
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''
INSERT INTO messages (user_id, message) VALUES (?, ?)''', (user_id, text))
    conn.commit()
    conn.close()

def getMessages():
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''
SELECT users.username, messages.message, users.avatar FROM users JOIN messages ON messages.user_id = users.id ORDER BY messages.id DESC''')
    messages = cursor.fetchall()
    conn.close()
    return messages

def deleteuser(username):
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''
                  UPDATE users SET username = ?, password = ?, avatar = ? WHERE username = ?''',("ANONYMUS", "JhftdDFftYTyfYFYfyFfF@#%&*(&%$1234243.V,CVL", "null", username,))
    conn.commit()

createMessages()
#addField()
#init_db()