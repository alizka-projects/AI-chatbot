import sqlite3
def connect():
    conn=sqlite3.connect("chatbot.db")
    return conn

def createTables():
    conn = connect()
    cursor = conn.cursor()
#===========chats===========
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS chats(
           chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
           title TEXT,
           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
         )
    """)

#=================MESSAGES============
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS messages(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           chat_id INTEGER,
           role TEXT,
           content TEXT,
           FOREIGN KEY(chat_id) REFERENCES chats(chat_id)
           )
    """)

    conn.commit()
    conn.close()


def create_chat():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""INSERT INTO chats (title) VALUES(?)""",("New Chat",))
    conn.commit()
    chat_id=cursor.lastrowid
    conn.close()
    return chat_id


def save_messages(chat_id,role,content):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""INSERT INTO messages (chat_id , role , content) VALUES(?,?,?)
""",(chat_id,role,content))
    conn.commit()
    conn.close()


def get_all():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""
        SELECT chat_id, title
        FROM chats
        ORDER BY created_at DESC """)
    chats= cursor.fetchall()
    conn.close()
    return chats

def get_messages(chat_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content
        FROM messages
        WHERE chat_id=?
        ORDER BY id
    """,(chat_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

    