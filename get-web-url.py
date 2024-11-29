from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# deploy ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# target url
url = "https://www.agedm.org/play/20240122/1/1"
driver.get(url)

try:
    # wait loading
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    
    # looking for iframe and switch to iframe
    iframe = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)

    # wait for video element
    video_elements = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "video"))
    )
    print("Found video element！")

    # looking for video tab and print out
    for video in video_elements:
        video_url = video.get_attribute("src")
        print(f"Video url: {video_url}")

finally:
    # turn off driver
    driver.quit()
