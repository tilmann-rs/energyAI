from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time


options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", '/data/Big Electricity')
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/csv")  # Automatically download CSVs

driver = webdriver.Firefox(options=options)
driver.get("https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/show")


wait = WebDriverWait(driver, 10)


try:
    agree_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='I Agree']")))
    agree_button.click()
except Exception as e:
    print(f"Cookies prompt not found or failed to click 'I Agree': {e}")


try:
    country_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Denmark (DK)']")))
    country_checkbox.click()
except Exception as e:
    print(f"Country checkbox not found: {e}")


for year in range(2015, 2023):
    try:

        calendar_button = wait.until(EC.element_to_be_clickable((By.ID, "calendar-button-id")))  # Update with actual ID or selector
        calendar_button.click()

        year_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@data-year='{year}']")))
        year_selector.click()

        day_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='1']")))
        day_button.click()

        done_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Done']")))
        done_button.click()

        export_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Actual Generation per Production Type (Year, CSV)")))
        export_button.click()

        time.sleep(10)

    except Exception as e:
        print(f"Error during processing for year {year}: {e}")


driver.quit()
