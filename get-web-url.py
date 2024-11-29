from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# input target url
url = input("url:")

# set Chrome hide
chrome_options = Options()
chrome_options.add_argument("--headless")  # hide

# deploy ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# driver get url
driver.get(url)

try:
    # wait for page loading
    print("wait for loading")
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # try to find video elements in the main page first
    print("looking for video elements in the main page")
    video_elements = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "video"))
    )
    
    # If video elements are found, print them
    if video_elements:
        print("Found video element(s) in the main page!")
        for video in video_elements:
            video_url = video.get_attribute("src")
            print(f"Video url: {video_url}")
    else:
        # If no video elements found in the main page, look for iframes and check for video inside
        print("No video element found in the main page, looking for iframe")
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        # Try to find video elements inside iframe
        print("looking for video elements in iframe")
        video_elements_iframe = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "video"))
        )
        if video_elements_iframe:
            print("Found video element(s) in iframe!")
            for video in video_elements_iframe:
                video_url = video.get_attribute("src")
                print(f"Video url: {video_url}")
        else:
            print("No video elements found in iframe either.")

finally:
    # turn off driver
    driver.quit()
