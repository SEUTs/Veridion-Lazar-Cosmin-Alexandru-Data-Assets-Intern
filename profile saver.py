import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

script_dir = os.path.dirname(os.path.abspath(__file__))
profile_path = os.path.join(script_dir, "selenium_profile")

options = Options()
options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.get("https://accounts.google.com/")

input("Aici intru in contul de google. Momentan asteapta. Dupa ce ma conectez, ii dau orice in input...")
driver.quit()
