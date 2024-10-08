import webbrowser
import time
from datetime import datetime
import schedule
import random
import threading
import os
import tkinter as tk
import psutil
from tkinter import messagebox

firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe"
webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

def get_desktop_path():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop, 'Songs.txt')

def read_urls_from_file():
    file_path = get_desktop_path() 
    songs = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(' - ')
                if len(parts) == 3:
                    song_name = f"{parts[0]} - {parts[1]}"
                    url = parts[2]
                    songs.append((song_name, url))
    else:
        print(f"{get_current_time()} -- Nema fajla: {file_path}")
    
    return songs

def open_youtube():
    songs = read_urls_from_file()
    if songs:
        song_name, url = random.choice(songs)
        uqwe = url.strip().split
        webbrowser.get('firefox').open(url)
        print(f"{get_current_time()} -- FireFox je pokrenut")
        print(f"{get_current_time()} -- Pustena je pesma: {song_name} - {url}")
    else:
        print(f"{get_current_time()} -- Playlista je prazna!")

def close_firefox():  
    for process in psutil.process_iter(['pid', 'name']):
        if 'firefox' in process.info['name'].lower():
            process.terminate()
    print(f"{get_current_time()} -- Firefox je ugasen")


def update_schedule(start_time, end_time):
    schedule.clear()

    schedule.every().day.at(start_time).do(open_youtube)
    schedule.every().day.at(end_time).do(close_firefox)

    print(f"{get_current_time()} -- Nov raspred: Start u {start_time}, kraj u {end_time}")

# Function triggered when 'Save' is pressed
def save_schedule():
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    
    if validate_time_format(start_time) and validate_time_format(end_time):
        update_schedule(start_time, end_time)
        messagebox.showinfo("Raspored snimljen", f"Nov raspored: Start u {start_time}, kraj u {end_time}")
    else:
        messagebox.showerror("Neispravan format", "Deder upiši u formatu HH:MM")

# Function to validate time format (HH:MM)
def validate_time_format(time_str):
    try:
        time.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def get_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time

# Function to continuously check and run scheduled tasks
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Tkinter GUI
root = tk.Tk()
root.title("Circus Beats")

# Start time input
start_label = tk.Label(root, text="Start")
start_label.grid(row=0, column=0, padx=10, pady=10)

start_time_entry = tk.Entry(root)
start_time_entry.grid(row=0, column=1, padx=10, pady=10)
start_time_entry.insert(0, "06:00") 

# End time input
end_label = tk.Label(root, text="Kraj")
end_label.grid(row=1, column=0, padx=10, pady=10)

end_time_entry = tk.Entry(root)
end_time_entry.grid(row=1, column=1, padx=10, pady=10)
end_time_entry.insert(0, "21:00")

# Save button
save_button = tk.Button(root, text="Snimi", command=save_schedule)
save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Start the schedule checking in a separate thread
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.daemon = True
schedule_thread.start()

# Start Tkinter main loop
root.mainloop()