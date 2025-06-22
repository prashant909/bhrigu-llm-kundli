import tkinter as tk
from tkinter import messagebox
import swisseph as swe
import pytz
import datetime
from geopy.geocoders import Nominatim

swe.set_ephe_path('./ephe')

def get_coordinates(place):
    geo = Nominatim(user_agent="kundli-app")
    location = geo.geocode(place)
    return location.latitude, location.longitude

def generate_kundli():
    dob = dob_entry.get()
    tob = tob_entry.get()
    pob = pob_entry.get()

    try:
        dt = datetime.datetime.strptime(dob + ' ' + tob, '%Y-%m-%d %H:%M')
        dt = pytz.timezone("Asia/Kolkata").localize(dt)
        utc = dt.astimezone(pytz.utc)
        jd = swe.julday(utc.year, utc.month, utc.day, utc.hour + utc.minute / 60)
        lat, lon = get_coordinates(pob)
        houses, ascmc = swe.houses(jd, lat, lon)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    result = f"Ascendant (Lagna): {ascmc[0]:.2f}°\n"
    result += "12 Houses:\n"
    for i, h in enumerate(houses):
        result += f"House {i+1}: {h:.2f}°\n"

    output.delete("1.0", tk.END)
    output.insert(tk.END, result)

root = tk.Tk()
root.title("Kundli Generator")

tk.Label(root, text="Date of Birth (YYYY-MM-DD):").pack()
dob_entry = tk.Entry(root)
dob_entry.pack()

tk.Label(root, text="Time of Birth (HH:MM):").pack()
tob_entry = tk.Entry(root)
tob_entry.pack()

tk.Label(root, text="Place of Birth:").pack()
pob_entry = tk.Entry(root)
pob_entry.pack()

tk.Button(root, text="Generate Kundli", command=generate_kundli).pack()
output = tk.Text(root, height=15)
output.pack()

root.mainloop()
