import sqlite3
import hashlib

# Connect to SQLite database (creates it if not exists)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    hashed = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print("✅ Registration successful!")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    result = cursor.fetchone()

    if result:
        print("✅ Login successful!")
    else:
        print("❌ Invalid username or password.")

def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print("❌ Invalid option, please try again.")

if __name__ == "__main__":
    main()
    conn.close()
