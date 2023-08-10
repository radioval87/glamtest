import asyncio
import logging
import os
import time

from envparse import Env
from fastapi import HTTPException
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env = Env()
env_file_path = os.path.join(BASE_DIR, ".env")
env.read_envfile(env_file_path)
logger = logging.getLogger()

PARSER_PROFILE_USERNAME = env.str("PARSER_PROFILE_USERNAME")
PARSER_PROFILE_PASSWORD = env.str("PARSER_PROFILE_PASSWORD")


def login_to_instagram(driver: webdriver.Chrome):
    driver.get("https://www.instagram.com")
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

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()

    # clicking through starting windows
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Not Now")]'))
    ).click()

    # not used when running in headless mode
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))
    # ).click()
    logger.info('Logging in successful')


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


def run_scraping(username: str, max_count: int):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options)
    try:
        login_to_instagram(driver)
    except Exception as e:
        logger.error('Logging in failed. Saving error.png')
        driver.save_screenshot('error.png')
        logger.error(e.with_traceback(e.__traceback__))
        raise HTTPException(status_code=400, detail=str(e))

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
        logger.info(f'Scraped {len(urls)} urls')
    driver.close()
    return urls[:max_count]


async def scrape_pic_urls(username: str, max_count: int):
    answer = await asyncio.to_thread(
        run_scraping,
        username,
        max_count
    )
    return answer
