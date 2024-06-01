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
    driver.get("https://titan22.com/account/login?return_url=%2Faccount")

    return driver

def main():
    driver = get_driver()
    driver.find_element(By.ID, value="CustomerEmail").send_keys("oussamaayari2014@gmail.com")
    time.sleep(2)
    driver.find_element(By.ID, value="CustomerPassword").send_keys("v_$dFK72$H*bVBS" + Keys.RETURN)
    time.sleep(2)
    driver.find_element(By.XPATH, value="/html/body/footer/div/section/div/div[1]/div[1]/div[1]/nav/ul/li[1]/a").click()
    time.sleep(10)
    print(driver.current_url)

if __name__ == "__main__":
    print(main())
