import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

# ---------------- BMI FUNCTIONS ----------------
def calculate_bmi():
    try:
        name = entry_name.get()
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if name == "":
            raise ValueError("Name required")

        if weight <= 0 or height <= 0 or height > 2.5:
            raise ValueError("Invalid range")

        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        category = get_category(bmi)

        label_result.config(
            text=f"BMI: {bmi}\nCategory: {category}",
            fg="green"
        )

        save_data(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid values\nHeight in meters (e.g. 1.70)"
        )

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# ---------------- DATA STORAGE ----------------
def save_data(name, weight, height, bmi, category):
    date = datetime.date.today().isoformat()
    cursor.execute(
        "INSERT INTO bmi_records (name, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
        (name, weight, height, bmi, category, date)
    )
    conn.commit()

# ---------------- VIEW HISTORY ----------------
def view_history():
    name = entry_name.get()
    cursor.execute("SELECT date, bmi FROM bmi_records WHERE name=?", (name,))
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("No Data", "No records found for this user")
        return

    history = ""
    for r in records:
        history += f"{r[0]}  →  BMI: {r[1]}\n"

    messagebox.showinfo("BMI History", history)

# ---------------- BMI GRAPH ----------------
def show_graph():
    name = entry_name.get()
    cursor.execute("SELECT date, bmi FROM bmi_records WHERE name=?", (name,))
    records = cursor.fetchall()

    if len(records) < 2:
        messagebox.showinfo("Not Enough Data", "Need at least 2 records")
        return

    dates = [r[0] for r in records]
    bmis = [r[1] for r in records]

    plt.figure()
    plt.plot(dates, bmis, marker='o')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title(f"BMI Trend for {name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ---------------- GUI DESIGN ----------------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x400")

tk.Label(root, text="BMI Calculator", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Weight (kg)").pack()
entry_weight = tk.Entry(root)
entry_weight.pack()

tk.Label(root, text="Height (meters)").pack()
entry_height = tk.Entry(root)
entry_height.pack()

tk.Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=10)

label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.pack()

tk.Button(root, text="View History", command=view_history).pack(pady=5)
tk.Button(root, text="Show BMI Graph", command=show_graph).pack(pady=5)

tk.Label(
    root,
    text="Height example: 1.70 meters",
    fg="gray"
).pack(pady=10)

root.mainloop()
