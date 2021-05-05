import sqlite3
import threading

connection = None
cursor = None 

def initialize_database():
    global connection, cursor

    connection = sqlite3.connect("storage.db", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='frames'")
    if cursor.fetchone()[0] != 1:
        cursor.execute('''CREATE TABLE frames (year number, month number, day number, hour number, src blob,
                        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)''')

        connection.commit()

def save_frame(date, encoded_frame):
    cursor.execute("INSERT INTO frames (year, month, day, hour, src) VALUES(?, ?, ?, ?, ?)", 
                    (date.year, date.month, date.day, date.hour, f"data:image/jpg;base64,{encoded_frame}"))

    connection.commit()

def close_database():
    connection.close()
    connection = None
    cursor = None

def get_saved_frames(count):
    if count == -1:
        cursor.execute("SELECT * FROM frames ORDER BY time DESC") 
    else:
        cursor.execute(f"SELECT * FROM frames ORDER BY time DESC LIMIT {count}") 

    result = cursor.fetchall()
    result_objects = []

    for row in result:
        result_objects.append({ "year": row[0], "month": row[1], "day": row[2], 
        "hour": row[3], "src": row[4]})

    return result_objects
