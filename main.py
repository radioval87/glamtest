import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


driver.get(f"https://www.instagram.com/therock/")

for _ in range(1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

imgaes = driver.find_elements(By.XPATH, '//div[@class="_aagv"]/img')
urls = [image.get_attribute('src') for image in imgaes]

print(urls)
