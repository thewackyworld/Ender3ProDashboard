import sqlite3

def init_db():
    conn = sqlite3.connect("printer_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS printer_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        nozzle_temp REAL,
        bed_temp REAL,
        status TEXT,
        progress REAL
    )
    """)

    conn.commit()

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_status ON printer_data(status);
    """)
    
    conn.commit()
    conn.close()

def insert_data(timestamp, nozzle, bed, status, progress):
    conn = sqlite3.connect("printer_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO printer_data (timestamp, nozzle_temp, bed_temp, status, progress)
    VALUES (?, ?, ?, ?, ?)
    """, (timestamp, nozzle, bed, status, progress))

    conn.commit()
    conn.close()