import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


SELENIUM_DRIVER_PATH = None
PARSER_PROFILE_USERNAME = None
PARSER_PROFILE_PASSWORD = None


def login_to_instagram(driver):
    driver.get(f"https://www.instagram.com")
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
    )
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
    )

    username.clear()
    username.send_keys(PARSER_PROFILE_USERNAME)

    password.clear()
    password.send_keys(PARSER_PROFILE_PASSWORD)

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()

    # clicking through starting windows
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Not Now")]'))
    ).click()
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))
    ).click()


def get_urls(driver: webdriver.Chrome, urls: list):
    images_div = driver.find_elements(
        By.XPATH, '//div[@class="_aabd _aa8k  _al3l"]/a[1]'
    )
    for i_div in images_div:
        url: str = i_div.find_element(
            By.XPATH, './/div[@class="_aagv"]/img'
        ).get_attribute("src")
        video: list = i_div.find_elements(By.XPATH, './/*[@aria-label="Video"]')
        clip: list = i_div.find_elements(By.XPATH, './/*[@aria-label="Clip"]')
        if not (video or clip) and url not in urls:
            urls.append(url)


def scrape_pic_urls(username: str, max_count: int):
    driver = webdriver.Chrome()
    login_to_instagram(driver)
    driver.get(f"https://www.instagram.com/{username}/")

    urls = []
    last_height: int = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        get_urls(driver, urls)
        new_height: int = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or len(urls) > max_count:
            break
        last_height = new_height
    driver.close()
    return urls[:max_count]
