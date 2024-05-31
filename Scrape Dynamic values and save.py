from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime as dt

def get_driver():
    # set options to make browsing easier
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])


    service = Service(r'C:\Users\deadl\Desktop\SMP\Automate\src\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://automated.pythonanywhere.com")

    return driver


def clean_text(text):
    """Extract only the temprature from the text"""
    output = float(text.split(": ")[1])
    return output


def write_file(text):
    """"Write input text into a text file"""
    filename = f"{dt.now().strftime('%Y-%m-%d.%H-%M-%S')}.txt"
    with open(filename, "w") as file:
        file.write(text)


def main():
    driver = get_driver()
    while True:
        time.sleep(2)
        element = driver.find_element(By.XPATH, value="/html/body/div[1]/div/h1[2]")
        text = str(clean_text(element.text))
        write_file(text)

if __name__ == "__main__":
    print(main())

