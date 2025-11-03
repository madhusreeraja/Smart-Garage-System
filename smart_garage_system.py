# =====================================================
# SMART GARAGE SYSTEM (Flask Project)
# =====================================================
# Created by: [Your Names]
# College: [Your College Name]
# Year: 2nd Year CSE
# -----------------------------------------------------
# This project simulates a smart garage that automatically
# opens or closes based on car detection (simulated sensor).
# =====================================================

from flask import Flask, render_template, request, redirect, url_for
import threading
import time

app = Flask(__name__)

# ---------- GLOBAL VARIABLES ----------
garage_status = "CLOSED"    # door state
car_detected = False        # sensor simulation
auto_mode = True            # automatic mode

# ---------- BACKEND LOGIC ----------
def open_garage():
    global garage_status
    if garage_status != "OPEN":
        print("🚗 Opening Garage Door...")
        time.sleep(1)
        garage_status = "OPEN"
        print("✅ Garage Door is OPEN")

def close_garage():
    global garage_status
    if garage_status != "CLOSED":
        print("🚘 Closing Garage Door...")
        time.sleep(1)
        garage_status = "CLOSED"
        print("❌ Garage Door is CLOSED")

# Background thread simulating sensor activity
def sensor_simulation():
    global car_detected, auto_mode
    while True:
        if auto_mode:
            if car_detected and garage_status == "CLOSED":
                open_garage()
            elif not car_detected and garage_status == "OPEN":
                close_garage()
        time.sleep(2)

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template(
        "index.html",
        status=garage_status,
        sensor="CAR DETECTED" if car_detected else "NO CAR",
        mode="ON" if auto_mode else "OFF"
    )

@app.route("/open", methods=["POST"])
def open_route():
    open_garage()
    return redirect(url_for("home"))

@app.route("/close", methods=["POST"])
def close_route():
    close_garage()
    return redirect(url_for("home"))

@app.route("/toggle_auto", methods=["POST"])
def toggle_auto():
    global auto_mode
    auto_mode = not auto_mode
    print("🔁 Auto Mode:", "ON" if auto_mode else "OFF")
    return redirect(url_for("home"))

@app.route("/simulate_car", methods=["POST"])
def simulate_car():
    global car_detected
    car_detected = True
    print("🚘 Car detected by sensor")
    return redirect(url_for("home"))

@app.route("/simulate_leave", methods=["POST"])
def simulate_leave():
    global car_detected
    car_detected = False
    print("🏁 Car left the garage")
    return redirect(url_for("home"))

# ---------- MAIN ----------
if __name__ == "__main__":
    # Start background sensor thread
    t = threading.Thread(target=sensor_simulation, daemon=True)
    t.start()

    print("🚗 Starting Smart Garage System at http://127.0.0.1:5000/")
    app.run(debug=False)
    # -----------------------------------------------------
# 💾 DATABASE MANAGEMENT SYSTEM (DBMS) CORE CONCEPTS
# -----------------------------------------------------
import sqlite3

# Connect to the database (creates garage.db if not exists)
conn = sqlite3.connect('garage.db')
cursor = conn.cursor()

# 1️⃣ CREATE TABLE (Schema Definition)
cursor.execute('''
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_number TEXT UNIQUE,
    owner_name TEXT NOT NULL,
    entry_time TEXT,
    exit_time TEXT
)
''')

# 2️⃣ INSERT DATA (Add records)
try:
    conn = sqlite3.connect("garage.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            number TEXT NOT NULL,
            intime TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
except Exception as e:
    print("Error while creating database:", e)


@app.route("/")
def home():
    conn = sqlite3.connect("garage.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    conn.close()
    return render_template("index.html", vehicles=vehicles)


@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    owner = request.form["owner"]
    number = request.form["number"]
    intime = request.form["intime"]

    conn = sqlite3.connect("garage.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vehicles (owner, number, intime) VALUES (?, ?, ?)", (owner, number, intime))
# -------------------------------
# MySQL Database Connection (DBMS Feature)
# -------------------------------

import mysql.connector

def mysql_connection_example():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password",  # replace with your actual MySQL password
            database="smart_garage"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS vehicles (id INT AUTO_INCREMENT PRIMARY KEY, owner VARCHAR(100), number VARCHAR(50), intime VARCHAR(50), outtime VARCHAR(50))")
        print("✅ MySQL connected and table created successfully!")
        conn.close()
    except Exception as e:
        print("❌ MySQL connection failed:", e)
# Demonstrate MySQL DBMS concept
mysql_connection_example()

if __name__ == "__main__":
    app.run(debug=True)

