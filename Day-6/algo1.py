import bcrypt
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    conn.commit()
    return conn

def register_user(conn, email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hashed)
        )
        conn.commit()
        print("Registrasi berhasil")
    except sqlite3.IntegrityError:
        print("Email sudah terdaftar")

def login_user(conn, email, password):
    row = conn.execute(
        "SELECT password_hash FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    if not row:
        print("Login gagal")
        return
    if bcrypt.checkpw(password.encode(), row[0]):
        print("Login berhasil")
    else:
        print("Login gagal")

if __name__ == "__main__":
    conn = init_db()
    register_user(conn, "user@example.com", "password123")
    login_user(conn, "user@example.com", "password123")
    login_user(conn, "user@example.com", "wrongpassword")
