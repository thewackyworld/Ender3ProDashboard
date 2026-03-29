from fastapi import FastAPI
from fastapi import Query
from dbcreate import init_db 
from dbcreate import insert_data
from PrinterAPIrequest import get_printer_data
import threading
import time
import sqlite3

latest_data = {}
app = FastAPI()
init_db()

def monitor_printer():
    while True:
        printer_data = get_printer_data()

        global latest_data
        latest_data = printer_data
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        insert_data(
            timestamp,
            printer_data["temperature"]["nozzle"]["actual"],
            printer_data["temperature"]["bed"]["actual"],
            printer_data["status"],
            printer_data["progress"] if printer_data["progress"] != "N/A" else None
        )

        time.sleep(5)  

@app.on_event("startup")
async def startup_event():
    monitor_thread = threading.Thread(target=monitor_printer, daemon=True)
    monitor_thread.start()

@app.get("/printer-status")
async def get_printer_status():
    return latest_data

@app.get("/history")
def get_history(limit: int = 50, status: str = None):
    conn = sqlite3.connect("printer_data.db")
    cursor = conn.cursor()

    query = "SELECT * FROM printer_data"
    params = []

    if status:
        query += " WHERE status = ?"
        params.append(status)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "timestamp": row[1],
            "nozzle": row[2],
            "bed": row[3],
            "status": row[4],
            "progress": row[5]
        }
        for row in rows
    ]

@app.get("/analytics")
def get_analytics():
    conn = sqlite3.connect("printer_data.db")
    cursor = conn.cursor()

    # Average temps
    cursor.execute("SELECT AVG(nozzle_temp), AVG(bed_temp) FROM printer_data")
    avg_nozzle, avg_bed = cursor.fetchone()

    # Total entries
    cursor.execute("SELECT COUNT(*) FROM printer_data")
    total_entries = cursor.fetchone()[0]

    # Printing entries
    cursor.execute("SELECT COUNT(*) FROM printer_data WHERE status = 'printing'")
    printing_entries = cursor.fetchone()[0]

    conn.close()

    return {
        "avg_nozzle_temp": round(avg_nozzle, 2) if avg_nozzle else None,
        "avg_bed_temp": round(avg_bed, 2) if avg_bed else None,
        "total_entries": total_entries,
        "printing_entries": printing_entries
    }

