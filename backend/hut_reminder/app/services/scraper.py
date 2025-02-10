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
from pprint import pprint


class Scraper:
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)

    # @classmethod
    # def new(cls):
    #     """Factory method to create a new Scraper instance"""
    #     return cls()

    def initialize_driver(self):
        """Set up and return a Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new') 
        options.add_argument('--disable-gpu')  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.driver.get("https://methowreservations.com/lodging/huts")
        self.logger.info("Browser initialized and navigated to the target site.")

    def select_winter_option(self):
        try: 
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "seasonal_year"))
            )
            select = Select(dropdown)
            select.select_by_visible_text("Winter 2024-2025")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))  
            )
            self.logger.info("Selected 'Winter' from the dropdown.")
        except (TimeoutException, WebDriverException) as e:
            self.logger.error(f"Error selecting winter option: {e}")

    # Step 6: Locate the table or hut data on the page
    def _locate_hut_names(self):
        try:
            tables = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
            )
            if not tables:
                self.logger.warning("No tables found.")
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
                        self.logger.error(f"Error locating hut names: {e}")

            return hut_names

        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            self.logger.error(f"Error locating hut names: {e}")
            return []

    def _locate_dates(self):
        try:
            tables = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
            )
            second_table = tables[1]

            first_row = second_table.find_element(By.TAG_NAME, "tr")
            cells = first_row.find_elements(By.TAG_NAME, "td")

            dates = []
            for cell in cells:
                date_text = cell.text.strip().split()[-1] 
                month = int(date_text.split('/')[0])
                day = int(date_text.split('/')[1])
                current_year = datetime.now().year
                # Might be a bug here for the years....
                year = current_year if month == 12 else current_year + 1 
                
                full_date = datetime.strptime(f"{year}-{month:02d}-{day:02d}", "%Y-%m-%d").date()
                dates.append(full_date)

            return dates
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Error locating dates: {e}")
            return []

    def locate_availability(self):
        try:
            # Get our list of hut names first
            hut_names = self._locate_hut_names()
            self.logger.info(f"Found {len(hut_names)} huts")
            
            # Get dates
            dates = self._locate_dates()
            if not dates:
                self.logger.error("No dates found in table")
                return []
            
            # Find the availability table
            tables = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
            )
            second_table = tables[1]
            rows = second_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
            
            availability_data = []
            for index, hut_name in enumerate(hut_names):
                if index >= len(rows): 
                    break
                
                row = rows[index]
                cells = row.find_elements(By.TAG_NAME, "td")
                
                hut_availability = {
                    "hut": hut_name,
                    "availability": {}
                }
                
                # Loop through each date cell
                for i, cell in enumerate(cells):
                    if i >= len(dates):  # Prevent index out of range
                        break
                    date = dates[i]
                    is_vacant = 'vacant' in cell.get_attribute('class').lower()
                    hut_availability["availability"][date] = is_vacant

                availability_data.append(hut_availability)

            return availability_data

        except Exception as e:
            self.logger.error(f"Error in locate_availability: {e}")
            return []

    def scrape(self):
        """Main method to perform the scraping operation"""
        try:
            self.initialize_driver()
            self.select_winter_option()
            availability = self.locate_availability()
            return availability
        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            return []
        finally:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = Scraper.new()
    result = scraper.scrape()
    pprint(result)
