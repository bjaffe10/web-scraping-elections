import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# Set up the WebDriver with headless Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)


# # Set up the WebDriver with normal Chrome
# driver = webdriver.Chrome()

url = "https://results.enr.clarityelections.com/CA/Marin/122487/web.345435/#/summary"
driver.get(url)
delay = 5 # seconds

# load page
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Last updated')]")))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")


# scroll to bottom of page
page_height = 0
old_page_height = 1

def show_height_and_scroll (delay):
    global page_height
    global old_page_height
    old_page_height = page_height
    page_height = driver.execute_script("return document.body.scrollHeight;")
    print("page height:", str(page_height))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(delay)

# count the number of page scrolls
counter = 0
while old_page_height != page_height:
    counter += 1
    print("counter:", str(counter))
    show_height_and_scroll(2)
    print("")

print("")    
print("**** **** top **** ****")
print(driver.page_source[0:200])
print("**** **** bottom **** ****")
print(driver.page_source[-200:])
print("")
print("total characters of html:" + str(len(driver.page_source)))
