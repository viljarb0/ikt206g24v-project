import psycopg
import hashlib
import bcrypt
import datetime

#conn_string = "host=localhost dbname=postgres user=postgres password=Password1."
conn_string = "dbname=postgres user=postgres password=Password1."


def list_users():
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            result = [x[0] for x in cur.fetchall()]
    return result

def verify(id, pw):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pw FROM users WHERE id = (%s)", (id.upper(),))
            db_pw = cur.fetchone()
            result = False
            if db_pw:
                result = bcrypt.checkpw(pw.encode(), db_pw[0])
    return result

def delete_user_from_db(id):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = (%s)", (id.upper(),))

    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE user = (%s)", (id.upper(),))

    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM images WHERE owner = (%s)", (id.upper(),))
 
def add_user(id, pw):
    if id.upper() not in list_users():
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                salt = bcrypt.gensalt()
                cur.execute(
                    "INSERT INTO users (id, pw) VALUES (%s, %s)",
                    (id.upper(), bcrypt.hashpw(pw.encode(), salt)))
 
def read_note_from_db(id):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT note_id, timestamp, note FROM notes WHERE username = (%s)", (id.upper(),))
            result = [x for x in cur.fetchall()]
    return result
   
def match_user_id_with_note_id(note_id):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user FROM notes WHERE note_id = (%s)", (note_id,))
            result = cur.fetchone()[0]
    return result
   
def write_note_into_db(id, note_to_write):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            current_timestamp = str(datetime.datetime.now())
            cur.execute("INSERT INTO notes (username, timestamp, note, note_id) VALUES (%s, %s, %s, %s)", (id.upper(), current_timestamp, note_to_write, hashlib.sha1((id.upper() + current_timestamp).encode()).hexdigest()))

def delete_note_from_db(note_id):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE note_id = (%s)", (note_id,))
 
def image_upload_record(uid, owner, image_name, timestamp):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO images (uid, owner, name, timestamp) VALUES (%s, %s, %s, %s)", (uid, owner, image_name, timestamp))
 
def list_images_for_user(owner):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT uid, timestamp, name FROM images WHERE owner = (%s)", (owner,))
            result = cur.fetchall()
    return result
   
def match_user_id_with_image_uid(image_uid):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT owner FROM images WHERE uid = (%s)", (image_uid,))
            result = cur.fetchone()[0]
    return result
   
def delete_image_from_db(image_uid):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM images WHERE uid = (%s)", (image_uid,))
   
def init_db():
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            #cur.execute("DROP TABLE IF EXISTS users;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id text,
                    pw text
                    )
                """)

            #cur.execute("DROP TABLE IF EXISTS notes;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    username text,
                    timestamp text,
                    note text,
                    note_id text
                    )
                """)

            #cur.execute("DROP TABLE IF EXISTS images;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    uid text,
                    owner text,
                    name text,
                    timestamp text
                    )
                """)
    add_user("ADMIN","admin")

if __name__ == "__main__":
    init_db()
    print(verify("admin", "admin"))
    print(list_users())

