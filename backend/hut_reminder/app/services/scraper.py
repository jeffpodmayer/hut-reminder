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
import time
import re
from datetime import timedelta


class Scraper:
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)

    @classmethod
    def new(cls):
        """Factory method to create a new Scraper instance"""
        return cls()

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
            select.select_by_visible_text("Winter 2025-26")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))  
            )
            self.logger.info("Selected 'Winter' from the dropdown.")
            print("Selected 'Winter 2025-26' from the dropdown.")
        except (TimeoutException, WebDriverException) as e:
            self.logger.error(f"Error selecting winter option: {e}")

    # Step 6: Locate the table or hut data on the page
    def _locate_hut_names(self):
        try:
            print("Locating hut names method called...")
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
            # Find the matrix scroll div which contains the table with dates
            matrix_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "matrixScroll"))
            )
            
            # Add a wait to allow dynamic content to load
            time.sleep(5)  # Wait 5 seconds for content to load
            
            # Look for date patterns in the page source
            page_source = self.driver.page_source
            
            date_patterns = re.findall(r'(\d{1,2}/\d{1,2})', page_source)
            print(f"Found {len(date_patterns)} date patterns in page source")
            
            # If we found date patterns, try to convert them to dates
            dates = []
            if date_patterns:
                for pattern in date_patterns:  # Process all patterns
                    try:
                        month, day = map(int, pattern.split('/'))
                        current_year = datetime.now().year
                        if month == 12:
                            year = current_year  
                        else:
                            year = current_year + 1
                        
                        full_date = datetime.strptime(f"{year}-{month:02d}-{day:02d}", "%Y-%m-%d").date()
                        dates.append(full_date)
                    except Exception:
                        # Just skip any errors
                        pass
            
            print(f"Successfully extracted {len(dates)} dates")
            
            # Validate the date range
            self.validate_date_range(dates)
            
            return dates
            
        except Exception as e:
            self.logger.error(f"Error locating dates: {e}")
            return []

    def validate_date_range(self, dates, start_month=12, start_day=12, end_month=3, end_day=15):
        """
        Validates that all dates between start_date and end_date are present in the dates list.
        
        Args:
            dates: List of datetime.date objects to validate
            start_month, start_day: Starting month and day
            end_month, end_day: Ending month and day
        
        Returns:
            Tuple of (is_complete, missing_dates)
        """
        if not dates:
            print("No dates to validate")
            return False, []
        
        # Sort the dates
        sorted_dates = sorted(dates)
        
        # Determine the years based on the first date in the list
        first_year = sorted_dates[0].year
        second_year = first_year + 1 if sorted_dates[0].month == 12 else first_year
        
        # Create start and end dates
        start_date = datetime(first_year, start_month, start_day).date()
        end_date = datetime(second_year, end_month, end_day).date()
        
        print(f"Validating dates from {start_date} to {end_date}")
        
        # Generate all dates in the range
        all_dates = []
        current_date = start_date
        while current_date <= end_date:
            all_dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Find missing dates
        missing_dates = [date for date in all_dates if date not in sorted_dates]
        
        # Report results
        if missing_dates:
            print(f"Missing {len(missing_dates)} dates:")
            for date in missing_dates[:10]:  # Show first 10 missing dates
                print(f"  - {date}")
            if len(missing_dates) > 10:
                print(f"  ... and {len(missing_dates) - 10} more")
        else:
            print("All dates in range are present!")
        
        return len(missing_dates) == 0, missing_dates

    def locate_availability(self):
        try:
            # Get our list of hut names first
            print("Locating hut names...")
            hut_names = self._locate_hut_names()
            print(f"Found {len(hut_names)} huts")
            self.logger.info(f"Found {len(hut_names)} huts")
            
            # Get dates
            dates = self._locate_dates()
            if not dates:

                self.logger.error("ERR:No dates found in table")
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
            
            # Call locate_availability to get both hut names and their availability
            availability_data = self.locate_availability()  # This now includes hut names
            hut_names = [entry['hut'] for entry in availability_data]  # Extract hut names from availability data
            
            return hut_names, availability_data  # Return both hut names and availability data
        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            return [], []  # Return empty lists on error
        finally:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = Scraper.new()
    result = scraper.scrape()
    pprint(result)
