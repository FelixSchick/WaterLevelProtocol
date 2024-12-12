import schedule
import time
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import base64
import re

print("Start screenshoting... 1.5")

def take_screenshot():
    today = datetime.now().strftime("%Y-%m-%d")
    folder_path = f"screenshots/{today}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.hochwasser.rlp.de/flussgebiet/mosel/wasserbillig")
    time.sleep(2)  # Warte etwas länger, um sicherzustellen, dass die Seite vollständig geladen ist

    time.sleep(5)  # Warte 5 Sekunden, um sicherzustellen, dass die Seite vollständig geladen ist

    # Klicke auf den Button, um das Bild herunterzuladen
    button = driver.find_element(By.CSS_SELECTOR, '.e-detail-chart__legend__save-chart-link')
    button.click()

    # Warte, bis das Bild heruntergeladen wird (optional, je nach Ladezeiten)
    time.sleep(5)  # Warte 5 Sekunden, um sicherzustellen, dass der Download abgeschlossen ist

    # Finde das Element, das den Base64-Link enthält (falls es sich ändert nach dem Klick)
    download_link_element = driver.find_element(By.CSS_SELECTOR, '.e-detail-chart__legend__save-chart-link')
    href_value = download_link_element.get_attribute('href')


    # Extrahiere den Base64-String aus dem href
    base64_data = re.sub('^data:image/png;base64,', '', href_value)
    
    # Decodiere den Base64-String
    image_data = base64.b64decode(base64_data)

    # Speichere die PNG-Datei

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"{folder_path}/screenshot_{now}.png"
    print(now)

    with open(filename, 'wb') as file:
        file.write(image_data)
    with open("current.png", 'wb') as file:
        file.write(image_data)
    driver.quit()

schedule.every().hour.do(take_screenshot)

# Developer Option:
#schedule.every().minute.do(take_screenshot)

while True:
    schedule.run_pending()
    time.sleep(1)
