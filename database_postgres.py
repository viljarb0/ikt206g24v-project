import os
import psycopg
import hashlib
import bcrypt
import datetime
import time

conn_list = []
try:
    psql_dbname = os.environ["POSTGRES_DB"]
except KeyError:
    psql_dbname = "postgres"
finally:
    conn_list.append("dbname="+psql_dbname)

try:
    psql_user = os.environ["POSTGRES_USER"]
except KeyError:
    psql_user = "postgres"
finally:
    conn_list.append("user="+psql_user)

try:
    psql_password = os.environ["POSTGRES_PASSWORD"]
except KeyError:
    psql_password = "Password1."
finally:
    conn_list.append("password="+psql_password)

try:
    psql_host = os.environ["POSTGRES_HOST"]
    conn_list.append("host="+psql_host)
except KeyError:
    pass

#conn_string = "host=172.16.241.10 dbname=postgres user=postgres password=Password1."
#conn_string = "host=172.17.0.1 dbname=postgres user=postgres password=Password1."
#conn_string = "host=172.16.241.11 dbname=postgres user=postgres password=Password1."
conn_string = " ".join(conn_list)

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
                encrypted_pw = db_pw[0].encode()
                encoded_pw = pw.encode()
                result = bcrypt.checkpw(encoded_pw, encrypted_pw)
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
                encoded_pw = pw.encode()
                salt = bcrypt.gensalt()
                encrypted_pw = bcrypt.hashpw(password=encoded_pw, salt=salt)
                cur.execute(
                    "INSERT INTO users (id, pw) VALUES (%s, %s)",
                    (id.upper(), encrypted_pw.decode()))


def read_note_from_db(id):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT note_id, timestamp, note FROM notes WHERE username = (%s)", (id.upper(),))
            result = [x for x in cur.fetchall()]
    return result


def match_user_id_with_note_id(note_id):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user FROM notes WHERE note_id = (%s)", (note_id,))
            result = cur.fetchone()[0]
    return result


def write_note_into_db(id, note_to_write):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            current_timestamp = str(datetime.datetime.now())
            cur.execute("INSERT INTO notes (username, timestamp, note, note_id) VALUES (%s, %s, %s, %s)", (id.upper(
            ), current_timestamp, note_to_write, hashlib.sha1((id.upper() + current_timestamp).encode()).hexdigest()))


def delete_note_from_db(note_id):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE note_id = (%s)", (note_id,))


def image_upload_record(uid, owner, image_name, timestamp):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO images (uid, owner, name, timestamp) VALUES (%s, %s, %s, %s)",
                        (uid, owner, image_name, timestamp))


def list_images_for_user(owner):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT uid, timestamp, name FROM images WHERE owner = (%s)", (owner,))
            result = cur.fetchall()
    return result


def match_user_id_with_image_uid(image_uid):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT owner FROM images WHERE uid = (%s)", (image_uid,))
            result = cur.fetchone()[0]
    return result


def delete_image_from_db(image_uid):
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM images WHERE uid = (%s)", (image_uid,))


def init_db():
    while True:
        try:
            with psycopg.connect(conn_string) as conn:
                break
        except Exception:
            pass
        time.sleep(3)
        print(f"Failed to connect to database using the connection: {conn_string}")

    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS users;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id text,
                    pw text
                    )
                """)

            cur.execute("DROP TABLE IF EXISTS notes;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    username text,
                    timestamp text,
                    note text,
                    note_id text
                    )
                """)

            cur.execute("DROP TABLE IF EXISTS images;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    uid text,
                    owner text,
                    name text,
                    timestamp text
                    )
                """)
    add_user("ADMIN", "admin")


if __name__ == "__main__":
    init_db()
    verify("admin", "admin")
