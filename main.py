from fastapi import FastAPI
from dbcreate import init_db 
from dbcreate import insert_data
from PrinterAPIrequest import get_printer_data
import threading
import time
import sqlite3

history = []
latest_data = {}
app = FastAPI()
init_db()

def monitor_printer():
    while True:
        printer_data = get_printer_data()
        data_point = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        **printer_data }

        global latest_data
        latest_data = printer_data

        history.append(data_point)
        if len(history) > 100:
            history.pop(0)
        print(len(history))

        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        insert_data(
            timestamp,
            printer_data["temperature"]["nozzle"]["actual"],
            printer_data["temperature"]["bed"]["actual"],
            printer_data["status"],
            printer_data["progress"] if printer_data["progress"] != "N/A" else None
        )

        time.sleep(5)  

@app.get("/printer-status")
async def get_printer_status():
    return latest_data

@app.get("/history")
def get_history():
    conn = sqlite3.connect("printer_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM printer_data ORDER BY id DESC LIMIT 50")
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

@app.on_event("startup")
async def startup_event():
    monitor_thread = threading.Thread(target=monitor_printer, daemon=True)
    monitor_thread.start()