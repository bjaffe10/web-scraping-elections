import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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
    myElem = WebDriverWait(driver, delay).until(ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Last updated')]")))
    print("Page appears to be loading...\n")
except TimeoutException:
    print("Loading took too much time!")


# scroll to bottom of page
page_height = 0
old_page_height = 1

def show_height_and_scroll (delay_sec):
    global page_height
    global old_page_height
    old_page_height = page_height
    page_height = driver.execute_script("return document.body.scrollHeight;")
    print("page height:", str(page_height))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(delay_sec)

# count the number of page scrolls
counter = 0
while old_page_height != page_height:
    counter += 1
    print("counter:", str(counter))
    show_height_and_scroll(2)
    print("")

time.sleep(4) # seconds
print("Page load complete. Scraping data...\n")

# Extract all races
races = driver.find_elements(By.CLASS_NAME, "card.contest")
print("Number of races:", str(len(races)), "\n")

# Dictionary to store results
election_data = {"races": []}

for race in races:
    # Extract race title and number of votes allowed by each person
    race_title = race.find_element(By.CLASS_NAME, "contest-name").text.strip()
    votes_per_person = int(race.find_element(By.CLASS_NAME, "fss.text-nowrap").find_elements(By.TAG_NAME, "strong")[0].text)

    # Extract candidates & vote counts
    candidate_rows = race.find_elements(By.CLASS_NAME, "row.align-items-top")

    results = []
    for candidate_row in candidate_rows:
        try:
            party = candidate_row.find_element(By.CLASS_NAME, "badge.bg-info.party-name").text
            name = candidate_row.find_element(By.CLASS_NAME, "col-6.d-inline-flex.col-9").find_elements(By.TAG_NAME, "div")[1].text
            votes = int(candidate_row.find_elements(By.CLASS_NAME, "col.text-end.pl-0")[1].text.strip().replace(",", ""))
            results.append({"candidate": name, "party": party, "votes": votes})
        except:
            continue  # Skip any malformed entries

    election_data["races"].append({"race_title": race_title, "votes_per_person": votes_per_person, "results": results})

for race in election_data["races"]:

    print(f"{race['race_title']} ({race['votes_per_person']} vote(s) per person)")
    for candidate in sorted(race["results"], key=lambda d: d['votes'], reverse=True):
        if candidate["party"] not in [None, " ", ""]:
            party = " (" + candidate["party"] + ")"
        else:
            party = ""
        print("   ", '{:<30}  {:>7}'.format(f"{candidate['candidate']}{party}:", f"{candidate['votes']:,}"))
    print()

# print("Complete election data:\n")
# print(json.dumps(election_data, indent=4))