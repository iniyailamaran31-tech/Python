import tkinter as tk
from tkinter import messagebox
import requests

# ---------------- CONFIG ----------------
API_KEY = "a853c04e05e23d4e59aa43db71f2f5a0"   # Replace with your OpenWeather API key

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return

    unit = unit_var.get()
    units = "metric" if unit == "Celsius" else "imperial"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"].title()

        unit_symbol = "°C" if unit == "Celsius" else "°F"
        wind_unit = "m/s" if unit == "Celsius" else "mph"

        result_label.config(
            text=f"🌍 City: {city}\n\n"
                 f"🌡 Temperature: {temp}{unit_symbol}\n"
                 f"☁ Condition: {desc}\n"
                 f"💧 Humidity: {humidity}%\n"
                 f"🌬 Wind Speed: {wind} {wind_unit}"
        )

    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data")

# GUI Window
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("420x450")
root.resizable(False, False)

# Title
tk.Label(root, text="🌦️ Weather Application", font=("Arial", 16, "bold")).pack(pady=10)

# City Input
tk.Label(root, text="Enter City Name").pack()
city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

# Unit Selection
unit_var = tk.StringVar(value="Celsius")
tk.Label(root, text="Temperature Unit").pack(pady=5)
tk.Radiobutton(root, text="Celsius (°C)", variable=unit_var, value="Celsius").pack()
tk.Radiobutton(root, text="Fahrenheit (°F)", variable=unit_var, value="Fahrenheit").pack()

# Button
tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather).pack(pady=15)

# Result Display
result_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
result_label.pack(pady=10)

root.mainloop()
