import sqlite3

DB_NAME = "hisob_kalla.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Daromad jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daromad (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kalla_soni INTEGER NOT NULL,
        narx INTEGER NOT NULL,
        jami INTEGER NOT NULL,
        sana TEXT NOT NULL
    )
    """)

    # Harajat jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS harajat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        izoh TEXT NOT NULL,
        summa INTEGER NOT NULL,
        sana TEXT NOT NULL
    )
    """)

    # Kassa jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kassa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summa INTEGER NOT NULL,
        sana TEXT NOT NULL,
        izoh TEXT
    )
    """)

    # Qarzlar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qarzlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism TEXT NOT NULL,
        qarz_miqdori INTEGER NOT NULL,
        sana TEXT NOT NULL
    )
    """)

    # Bank jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summa INTEGER NOT NULL,
        sana TEXT NOT NULL,
        izoh TEXT
    )
    """)

    # Jamgarma jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jamgarma (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summa INTEGER NOT NULL,
        sana TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Barcha jadvallar muvaffaqiyatli yaratildi!")