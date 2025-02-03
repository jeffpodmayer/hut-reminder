from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime
import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step 1: Set up the Selenium WebDriver
# Step 2: Navigate to the target website 
def initialize_driver():
    """Set up and return a Selenium WebDriver."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://methowreservations.com/lodging/huts")
    logger.info("Browser initialized and navigated to the target site.")
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
    except (TimeoutException, WebDriverException) as e:
        logger.error(f"Error selecting winter option: {e}")

# Step 6: Locate the table or hut data on the page
def locate_hut_names(driver):
    """Locate hut names from the specified table structure."""
    try:
        tables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        if not tables:
            logger.warning("No tables found.")
            return []
        table = tables[0]       
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
                except NoSuchElementException as e:
                    continue
                except WebDriverException as e:
                    logger.error(f"Error locating hut names: {e}")

        return hut_names

    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Error locating hut names: {e}")
        return []

def locate_dates(driver):
    """Locate dates from the second table on the page."""
    try:
        tables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        second_table = tables[1]

        first_row = second_table.find_element(By.TAG_NAME, "tr")

        cells = first_row.find_elements(By.TAG_NAME, "td")

        dates = []
        for cell in cells:
            date_text = cell.text.strip().split()[-1] 
            date_obj = datetime.strptime(date_text, "%m/%d")
            current_year = datetime.now().year
            full_date = datetime.strptime(f"{current_year}-{date_obj.strftime('%m-%d')}", "%Y-%m-%d").date()
            dates.append(full_date)

        return dates
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"Error locating dates: {e}")
        return []

def locate_availability(driver):
    """Locate availability for each hut on the page."""
    try:
        # Get dates
        dates = locate_dates(driver)
        if not dates:
            logger.error("No dates found in table")
            return []
            
        # Find the availability table
        tables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        second_table = tables[1]
        rows = second_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
        
        availability_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if not cells:
                continue
            
            # Get hut name using the same approach as locate_hut_names
            try:
                first_cell = cells[0]
                span = first_cell.find_element(By.CLASS_NAME, "rooms")
                name_div = span.find_element(By.CLASS_NAME, "name")
                hut_name = name_div.text.strip()
                
                if not hut_name:
                    continue
                
                hut_availability = {
                    "hut": hut_name,
                    "availability": {}
                }
                
                # Loop through each date cell (skip first cell which is hut name)
                for i, cell in enumerate(cells[1:]):
                    if i >= len(dates):  # Prevent index out of range
                        break
                    date = dates[i]
                    is_vacant = 'vacant' in cell.get_attribute('class').lower()
                    hut_availability["availability"][date] = is_vacant

                availability_data.append(hut_availability)
                
            except NoSuchElementException:
                continue

        return availability_data

    except Exception as e:
        logger.error(f"Error in locate_availability: {e}")
        return []

# Store this in the DB in the Hut model
# Store into the Availabliity model?
# Step 8: Process or store the extracted data

if __name__ == "__main__":
    driver = initialize_driver()
    select_winter_option(driver)
    huts = locate_hut_names(driver)
    print("Hut Names:", huts)
    dates = locate_dates(driver)
    # print("Dates:", dates)
    
    # Get and print availability in a more readable format
    availability = locate_availability(driver)
    print("\n=== Availability Data ===")
    for hut_data in availability:
        print(f"\nHut: {hut_data['hut']}")
        print("Availability:")
        for date, is_vacant in hut_data['availability'].items():
            print(f"  {date}: {'Available' if is_vacant else 'Not Available'}")
    
    driver.quit()
