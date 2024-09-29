import webbrowser
import time
import subprocess
import schedule
import random
import tkinter as tk
from tkinter import messagebox
import threading
import os

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def get_desktop_path():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop, 'Songs.txt')

def read_urls_from_file():
    file_path = get_desktop_path() 
    urls = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(' - ')
                if len(parts) == 3:
                    urls.append(parts[2])
    else:
        print(f"Nema fajla: {file_path}")
        
    return urls

def open_youtube():
    urls = read_urls_from_file()
    if urls:
        url = random.choice(urls)
        webbrowser.get('chrome').open(url)
    else:
        print("The playlist is empty!")

def close_chrome():
    subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])

# Function to update schedule with new times
def update_schedule(start_time, end_time):
    # Clear any previously set schedules
    schedule.clear()

    # Set new schedule with updated times
    schedule.every().day.at(start_time).do(open_youtube)
    schedule.every().day.at(end_time).do(close_chrome)

    print(f"New schedule set: Start at {start_time}, End at {end_time}")

# Function triggered when 'Save' is pressed
def save_schedule():
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    
    if validate_time_format(start_time) and validate_time_format(end_time):
        update_schedule(start_time, end_time)
        messagebox.showinfo("Schedule Updated", f"New schedule: Start at {start_time}, End at {end_time}")
    else:
        messagebox.showerror("Invalid Time Format", "Please enter time in the format HH:MM")

# Function to validate time format (HH:MM)
def validate_time_format(time_str):
    try:
        time.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# Function to continuously check and run scheduled tasks
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(0.1)

# Tkinter GUI
root = tk.Tk()
root.title("Circus Beats")

# Start time input
start_label = tk.Label(root, text="Start")
start_label.grid(row=0, column=0, padx=10, pady=10)

start_time_entry = tk.Entry(root)
start_time_entry.grid(row=0, column=1, padx=10, pady=10)
start_time_entry.insert(0, "06:00")  # Default start time

# End time input
end_label = tk.Label(root, text="End")
end_label.grid(row=1, column=0, padx=10, pady=10)

end_time_entry = tk.Entry(root)
end_time_entry.grid(row=1, column=1, padx=10, pady=10)
end_time_entry.insert(0, "00:15")  # Default end time

# Save button
save_button = tk.Button(root, text="Save", command=save_schedule)
save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Start the schedule checking in a separate thread
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.daemon = True
schedule_thread.start()

# Start Tkinter main loop
root.mainloop()