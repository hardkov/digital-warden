import sqlite3

connection = None
cursor = None 

def initialize_database():
    global connection, cursor

    connection = sqlite3.connect("storage.db", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='frames'")
    if cursor.fetchone()[0] != 1:
        cursor.execute('''CREATE TABLE frames (src blob,
                            created_at REAL)''')

        connection.commit()

def save_frame(timestamp, encoded_frame):
    cursor.execute("INSERT INTO frames (src, created_at) VALUES(?, ?)", 
                    (f"data:image/jpg;base64,{encoded_frame}", timestamp))

    connection.commit()

def close_database():
    connection.close()

def get_saved_frames(count):
    if count == -1:
        cursor.execute("SELECT * FROM frames ORDER BY created_at DESC") 
    else:
        cursor.execute(f"SELECT * FROM frames ORDER BY created_at DESC LIMIT {count}") 

    result = cursor.fetchall()
    result_objects = []

    for row in result:
        result_objects.append({"src": row[0], "created_at": row[1]})

    return result_objects
