import sqlite3
import hashlib
import bcrypt
import datetime

user_db_file_location = "database_file/users.db"
note_db_file_location = "database_file/notes.db"
image_db_file_location = "database_file/images.db"

def list_users():
    with sqlite3.connect(user_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("SELECT id FROM users;")
        result = [x[0] for x in _c.fetchall()]

    return result

def verify(id, pw):
    with sqlite3.connect(user_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("SELECT pw FROM users WHERE id = ?;", (id.upper(),))
        #result = _c.fetchone()[0] == hashlib.sha256(pw.encode()).hexdigest()
        db_pw = _c.fetchone()
        result = False
        if db_pw:
            result = bcrypt.checkpw(pw.encode(), db_pw[0])

    return result

def delete_user_from_db(id):
    with sqlite3.connect(user_db_file_location) as _conn:
        _c = _conn.cursor()
        _c.execute("DELETE FROM users WHERE id = ?;", (id.upper(),))
        _conn.commit()

    # when we delete a user FROM database USERS, we also need to delete all his or her notes data FROM database NOTES
    with sqlite3.connect(note_db_file_location) as _conn:
        _c = _conn.cursor()
        _c.execute("DELETE FROM notes WHERE user = ?;", (id.upper(),))
        _conn.commit()

    # when we delete a user FROM database USERS, we also need to 
    # [1] delete all his or her images FROM image pool (done in app.py)
    # [2] delete all his or her images records FROM database IMAGES
    with sqlite3.connect(image_db_file_location) as _conn:
        _c = _conn.cursor()
        _c.execute("DELETE FROM images WHERE owner = ?;", (id.upper(),))
        _conn.commit()

def add_user(id, pw):
    if id.upper() not in list_users():
        with sqlite3.connect(user_db_file_location) as _conn:
            _c = _conn.cursor()

            salt = bcrypt.gensalt()
            _c.execute("INSERT INTO users values(?, ?)", (id.upper(), bcrypt.hashpw(pw.encode(), salt)))
            
            _conn.commit()

def read_note_from_db(id):
    with sqlite3.connect(note_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("SELECT note_id, timestamp, note FROM notes WHERE user = ?;", (id.upper(),))
        result = _c.fetchall()

    return result

def match_user_id_with_note_id(note_id):
    # Given the note id, confirm if the current user is the owner of the note which is being operated.
    with sqlite3.connect(note_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("SELECT user FROM notes WHERE note_id = ?;", (note_id,))
        result = _c.fetchone()[0]

    return result

def write_note_into_db(id, note_to_write):
    with sqlite3.connect(note_db_file_location) as _conn:
        _c = _conn.cursor()

        current_timestamp = str(datetime.datetime.now())
        _c.execute("INSERT INTO notes values(?, ?, ?, ?)", (id.upper(), current_timestamp, note_to_write, hashlib.sha1((id.upper() + current_timestamp).encode()).hexdigest()))

        _conn.commit()

def delete_note_from_db(note_id):
    with sqlite3.connect(note_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("DELETE FROM notes WHERE note_id = ?;", (note_id,))

        _conn.commit()

def image_upload_record(uid, owner, image_name, timestamp):
    with sqlite3.connect(image_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("INSERT INTO images VALUES (?, ?, ?, ?)", (uid, owner, image_name, timestamp))

        _conn.commit()

def list_images_for_user(owner):
    with sqlite3.connect(image_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("SELECT uid, timestamp, name FROM images WHERE owner = ?;", (owner,))
        result = _c.fetchall()

    return result

def match_user_id_with_image_uid(image_uid):
    # Given the note id, confirm if the current user is the owner of the note which is being operated.
    with sqlite3.connect(image_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("SELECT owner FROM images WHERE uid = ?;", (image_uid,))
        result = _c.fetchone()[0]

    return result

def delete_image_from_db(image_uid):
    with sqlite3.connect(image_db_file_location) as _conn:
        _c = _conn.cursor()

        _c.execute("DELETE FROM images WHERE uid = ?;", (image_uid,))

        _conn.commit()

def init_db():
    with sqlite3.connect(user_db_file_location) as conn:
        cur = conn.cursor()
        cur.execute(
            "DROP TABLE IF EXISTS users"
            )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users(id TEXT, pw TEXT)")
        conn.commit()
    with sqlite3.connect(image_db_file_location) as conn:
        cur = conn.cursor()
        cur.execute(
            "DROP TABLE IF EXISTS images"
            )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS images(uid TEXT, owner TEXT, name TEXT, timestamp TEXT)")
        conn.commit()
    with sqlite3.connect(note_db_file_location) as conn:
        cur = conn.cursor()
        cur.execute(
            "DROP TABLE IF EXISTS notes"
            )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS notes(user TEXT, timestamp TEXT, note TEXT, note_id TEXT)")
        conn.commit()

    add_user("admin","admin")

if __name__ == "__main__":

    init_db()
    print(verify("admin","admin"))
    print(list_users())

