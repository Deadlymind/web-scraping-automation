from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

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
    driver.get("https://automated.pythonanywhere.com/login/")

    return driver

def clean_text(text):
    """Extract only the temperature from the text"""
    try:
        output = float(text.split(": ")[1])
        return output
    except (IndexError, ValueError) as e:
        print(f"Error extracting temperature: {e}")
        return None

def main():
    driver = get_driver()

    # find and fill in the user name and password
    driver.find_element(By.ID, value="id_username").send_keys("automated")
    time.sleep(2)
    driver.find_element(By.ID, value="id_password").send_keys("automatedautomated" + Keys.RETURN)
    time.sleep(2)

    # Click on Home link and wait 2 sec
    driver.find_element(By.XPATH, value="/html/body/nav/div/a").click()
    time.sleep(2)

    # Scrape the temperature value
    text = driver.find_element(By.XPATH, value="/html/body/div[1]/div/h1[2]").text
    print(f"Scraped text: '{text}'")  # print the scraped text for debugging

    # Clean the text
    return clean_text(text)

if __name__ == "__main__":
    result = main()
    if result is not None:
        print(f"Extracted temperature: {result}")
