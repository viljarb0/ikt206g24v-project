import psycopg
import hashlib
import datetime

user_db_file_location = "database_file/users.db"
note_db_file_location = "database_file/notes.db"
image_db_file_location = "database_file/images.db"
conn_string = "host=172.18.0.1 dbname=postgres user=postgres password=Password1."

def init_db():
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS users;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id text,
                    pw text)
                """)

def list_users():
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            result = [x for x in cur.fetchall()]
    return result

def verify(id, pw):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pw FROM users WHERE id = (%s)", (id.upper(),))
            result = cur.fetchone()[0] == hashlib.sha256(pw.encode()).hexdigest()
    return result

def delete_user_from_db(id):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = (%s)", (id.upper(),))

    # delete his notes too
 
def add_user(id, pw):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (id, pw) VALUES (%s, %s)",
                (id.upper(), hashlib.sha256(pw.encode()).hexdigest()))
   
def read_note_from_db(id):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            pass
   
def match_user_id_with_note_id(note_id):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            pass

   
def write_note_into_db(id, note_to_write):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            pass
   
def delete_note_from_db(note_id):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            pass
   
def image_upload_record(uid, owner, image_name, timestamp):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            pass
   
def list_images_for_user(owner):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            pass
   
def match_user_id_with_image_uid(image_uid):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            pass
   
def delete_image_from_db(image_uid):
     with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            pass
   

init_db()
add_user("user1","123")
print(verify("user1", "123"))
delete_user_from_db("user1")
add_user("user1","123")
print(list_users())

