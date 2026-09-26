import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import pyautogui
from random import randint
import winsound
import pandas as pd
import clipboard
import myModifier


def get_google_search_text(queries):
    # Aici ii dau setarile browser-ului si sa stie sa imi intre in contul meu de google
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    profile_path = os.path.join(script_dir, "selenium_profile")
    
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--profile-directory=Default") 

    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    try:
        driver.get("https://www.google.com")
        time.sleep(0.024) 

        index = 0
        for q in queries:
            print(f"SEARCHING FOR {index}: {q}")
            index += 1
            removed_quotes = q
            removed_quotes = removed_quotes.replace("\"", "")
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.71)
            pyautogui.press('\"')
            time.sleep(0.01 * randint(8, 24))
            clipboard.copy(q)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2356)
            # for c in f"{q} uk company vat":
            for c in f"\" uk company vat":
                pyautogui.press(c)
                time.sleep(0.01 * randint(8, 24))
            time.sleep(0.36)
            pyautogui.press('enter')

            time.sleep(1)
            while "not a robot" in driver.page_source:
                frequency = 2500
                duration = 3000
                # winsound.Beep(frequency, duration)
                time.sleep(duration / 1000 + 5)

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "MjjYud"))
            )
            time.sleep(3)
            modified_company_name = myModifier.modify(q)
            with open(f"company files/{modified_company_name}.html", 'w', encoding="utf-8") as f:
                f.write(driver.page_source)

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None
        
    finally:
        driver.quit()

if __name__ == "__main__":

    # de test, ignorate dupa
    companies = ["marks and spencer", "the social group limited"]
    to_search = []
    # A fost prea mare sa il urc pe github. Este 7 part 7 din septembrie 2026.
    df = pd.read_csv("Companies House initial dataset.csv", low_memory=False)
    for name in df.iloc[200:824, 0]:
        suffixless_name = myModifier.remove_suffixes(name)
        to_search.append(suffixless_name)
    print(to_search)
    get_google_search_text(to_search)
    