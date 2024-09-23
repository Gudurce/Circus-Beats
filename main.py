import webbrowser
import time
import subprocess
import schedule
import random

chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe" 

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def read_urls_from_file(file_path):
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) == 3:
                urls.append(parts[2])
    return urls
            
def open_youtube():
    urls = read_urls_from_file('Songs.txt')
    if urls:
        url = random.choice(urls)
        webbrowser.get('chrome').open(url)
    else:
        print("Lista je prazna!")
        
def close_chrome():
    subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    
schedule.every().day.at("23:50").do(open_youtube)
schedule.every().day.at("21:00").do(close_chrome)

while True:
    schedule.run_pending()
    time.sleep(60)