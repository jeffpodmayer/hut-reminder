from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

# Step 1: Set up the Selenium WebDriver
# Step 2: Navigate to the target website 
def initialize_driver():
    """Set up and return a Selenium WebDriver."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://methowreservations.com/lodging/huts")
    print("Browser initialized and navigated to the target site.")
    return driver

def select_winter_option(driver):
    """Select 'Winter' option from dropdown and wait for page to reload"""
    try: 
        # Step 3: Locate the dropdown menu 
        dropdown = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, "seasonal_year"))
        )
        # Step 4: Interact with the dropdown menu - ensure that the dropdown is selecting the "Winter" option
        select = Select(dropdown)
        select.select_by_visible_text("Winter 2024-2025")

        # Step 5: Wait for the page to update
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))  
        )
        print("Selected 'Winter' from the dropdown.")
    except Exception as e:
        print(e)

# Step 6: Locate the table or hut data on the page
def locate_hut_names(driver):
    """Locate hut names from the specified table structure."""
    try:
        tables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        if not tables:
            print("No tables found.")
            return []
        table = tables[0]  
        print("First table found.")
        
        rows = table.find_elements(By.TAG_NAME, "tr")

        hut_names = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")

            for cell in cells:
                try:
                    span = cell.find_element(By.CLASS_NAME, "rooms")
                    name_divs = span.find_elements(By.CLASS_NAME, "name")
                    for div in name_divs:
                        hut_names.append(div.text)
                except:
                    continue

        return hut_names

    except Exception as e:
        print(f"Error locating hut names: {e}")
        return []


# Store this in the DB in the Hut model
# might need to extract the hut name and dates of the columns from the table first?


# Step 7: Extract data from the table
# Go thrtough  header row and build an array of dates
# Go through each row hut to see if data is "filled" or "vacant" set boolean isVacant
# then need to go through each availability cell
# - Loop through the rows and cells of the table to extract the text or data you need


# Store into the Availabliity model?

# Step 8: Process or store the extracted data
# - Save the scraped data to a database? In the 


# Step 9: Close the WebDriver
# - After completing the scraping, close the browser session to free up system resources.

if __name__ == "__main__":
    driver = initialize_driver()
    select_winter_option(driver);
    huts = locate_hut_names(driver)
    print("Hut Names:", huts)
    driver.quit();
