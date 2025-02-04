import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, date
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from app.services.scraper import Scraper

class TestScraper(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scraper = Scraper.new()
        self.scraper.driver = MagicMock()
        self.scraper.logger = MagicMock()
        self.scraper.driver.current_url = "https://methowreservations.com/lodging/huts"
        self.scraper.driver.title = "Lodging in Winthrop, WA at Rendezvous Huts with Methow Reservations"

    def tearDown(self):
        """Clean up after each test method."""
        if hasattr(self.scraper, 'driver'):
            self.scraper.driver.quit()

    ## Testing the initialization of the Scraper class
    def test_initialization(self):
        """Test if Scraper initializes correctly."""
        self.assertIsInstance(self.scraper, Scraper)
        self.assertIsNotNone(self.scraper.logger)

    #Testing the select_winter_option method
    def test_select_winter_option_success(self):
        """Test successful winter option selection."""
        mock_dropdown = MagicMock()
        mock_select = MagicMock()
        
        # Mock the Select class
        with patch('app.services.scraper.Select') as mock_select_class:
            mock_select_class.return_value = mock_select
            
            # Mock WebDriverWait
            with patch('app.services.scraper.WebDriverWait') as mock_wait:
                # Set up the wait.until to return our mock dropdown
                mock_wait.return_value.until.side_effect = [mock_dropdown, None]
                # Run the method
                self.scraper.select_winter_option()
                assert mock_wait.return_value.until.call_count == 2
                mock_select_class.assert_called_once_with(mock_dropdown)
                mock_select.select_by_visible_text.assert_called_once_with("Winter 2024-2025")

    def test_select_winter_option_timeout(self):
        """Test handling of TimeoutException."""
        # Mock WebDriverWait to raise TimeoutException
        mock_wait = MagicMock()
        mock_wait.until.side_effect = TimeoutException("Element not found")
        
        with patch('selenium.webdriver.support.wait.WebDriverWait', return_value=mock_wait):
            self.scraper.select_winter_option()
            
            # Verify error was logged
            self.scraper.logger.error.assert_called_once()
            error_message = self.scraper.logger.error.call_args[0][0]
            self.assertIn("Error selecting winter option", error_message)

    def test_select_winter_option_webdriver_exception(self):
        """Test handling of WebDriverException."""
        # Mock WebDriverWait to raise WebDriverException
        mock_wait = MagicMock()
        mock_wait.until.side_effect = WebDriverException("Browser error")
        
        with patch('selenium.webdriver.support.wait.WebDriverWait', return_value=mock_wait):
            self.scraper.select_winter_option()
            
            # Verify error was logged
            self.scraper.logger.error.assert_called_once()
            error_message = self.scraper.logger.error.call_args[0][0]
            self.assertIn("Error selecting winter option", error_message)

    def test_locate_hut_names_success(self):
        """Test successful hut name location."""
        # Create mock elements
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_cell = MagicMock()
        mock_span = MagicMock()
        mock_div = MagicMock()
        
        # Set up mock chain
        mock_div.text = "Test Hut"
        mock_span.find_elements.return_value = [mock_div]
        mock_cell.find_element.return_value = mock_span
        mock_row.find_elements.return_value = [mock_cell]
        mock_table.find_elements.return_value = [mock_row]
        
        with patch('app.services.scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = [mock_table]
            
            # Run the method
            result = self.scraper._locate_hut_names()
            # Verify results
            self.assertEqual(result, ["Test Hut"])
            mock_wait.return_value.until.assert_called_once()
            mock_table.find_elements.assert_called_with(By.TAG_NAME, "tr")

    def test_locate_hut_names_no_tables(self):
        """Test when no tables are found."""
        with patch('app.services.scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = []
            # Run the method
            result = self.scraper._locate_hut_names()
            
            self.assertEqual(result, [])
            self.scraper.logger.warning.assert_called_with("No tables found.")

    def test_locate_hut_names_element_not_found(self):
        """Test handling of NoSuchElementException."""
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_cell = MagicMock()
        
        # Set up the exception
        mock_cell.find_element.side_effect = NoSuchElementException("Element not found")
        mock_row.find_elements.return_value = [mock_cell]
        mock_table.find_elements.return_value = [mock_row]
        
        with patch('app.services.scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = [mock_table]
            #Run the method
            result = self.scraper._locate_hut_names()
            #Verify results
            self.assertEqual(result, [])

    def test_locate_hut_names_webdriver_exception(self):
        """Test handling of WebDriverException."""
        with patch('app.services.scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.side_effect = WebDriverException("Browser error")
            # Run the method           
            result = self.scraper._locate_hut_names()
            # Verify results    
            self.assertEqual(result, [])
            self.scraper.logger.error.assert_called_once()
            error_message = self.scraper.logger.error.call_args[0][0]
            self.assertIn("Error locating hut names", error_message)

    def test_locate_dates_success(self):
        """Test successful date location and parsing."""
        # Create mock elements
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_cell = MagicMock()
        
        # Set up mock data
        mock_cell.text = "Thu 12/25"  # Example date
        mock_row.find_elements.return_value = [mock_cell]
        mock_table.find_element.return_value = mock_row
        
        # Mock WebDriverWait
        with patch('app.services.scraper.WebDriverWait') as mock_wait:
            # Return two tables, we need the second one (index 1)
            mock_wait.return_value.until.return_value = [MagicMock(), mock_table]
            
            # Mock datetime.now() to return a specific date for consistent testing
            with patch('app.services.scraper.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 11, 1)  # Set current date
                mock_datetime.strptime = datetime.strptime  # Keep original strptime
                
                # Run the method
                result = self.scraper._locate_dates()
                
                # Verify results
                self.assertEqual(len(result), 1)
                self.assertIsInstance(result[0], date)
                self.assertEqual(result[0], date(2024, 12, 25))

    def test_locate_dates_multiple_dates(self):
        """Test parsing multiple dates."""
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_cell1 = MagicMock(text="Thu 12/25")
        mock_cell2 = MagicMock(text="Fri 1/15")
        
        mock_row.find_elements.return_value = [mock_cell1, mock_cell2]
        mock_table.find_element.return_value = mock_row
        
        with patch('app.services.scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = [MagicMock(), mock_table]
            
            with patch('app.services.scraper.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 11, 1)
                mock_datetime.strptime = datetime.strptime
                
                result = self.scraper._locate_dates()
                
                self.assertEqual(len(result), 2)
                self.assertEqual(result[0], date(2024, 12, 25))
                self.assertEqual(result[1], date(2025, 1, 15))

    def test_locate_dates_no_tables(self):
        """Test when tables aren't found."""
        with patch('app.services.scraper.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.side_effect = TimeoutException("No tables found")
            
            result = self.scraper._locate_dates()
            
            self.assertEqual(result, [])
            self.scraper.logger.error.assert_called_once()
            error_message = self.scraper.logger.error.call_args[0][0]
            self.assertIn("Error locating dates", error_message)

    def test_locate_availability_success(self):
        """Test successful availability location."""
        # Mock the helper methods
        mock_hut_names = ["Hut1", "Hut2"]
        mock_dates = [date(2024, 12, 25), date(2024, 12, 26)]
        
        # Create mock elements for availability table
        mock_table = MagicMock()
        mock_row1 = MagicMock()
        mock_row2 = MagicMock()
        
        # Create mock cells with different availability states
        mock_cell_vacant = MagicMock()
        mock_cell_vacant.get_attribute.return_value = "vacant"
        mock_cell_occupied = MagicMock()
        mock_cell_occupied.get_attribute.return_value = "occupied"
        
        # Set up rows with cells
        mock_row1.find_elements.return_value = [mock_cell_vacant, mock_cell_occupied]
        mock_row2.find_elements.return_value = [mock_cell_occupied, mock_cell_vacant]
        
        with patch.object(self.scraper, '_locate_hut_names', return_value=mock_hut_names), \
             patch.object(self.scraper, '_locate_dates', return_value=mock_dates), \
             patch('app.services.scraper.WebDriverWait') as mock_wait:
            
            # Mock the availability table
            mock_wait.return_value.until.return_value = [MagicMock(), mock_table]
            mock_table.find_elements.return_value = [MagicMock(), mock_row1, mock_row2]  # First row is header
            
            # Run the method
            result = self.scraper.locate_availability()
            
            # Verify results
            self.assertEqual(len(result), 2)  # Two huts
            
            # Check first hut
            self.assertEqual(result[0]["hut"], "Hut1")
            self.assertEqual(result[0]["availability"][mock_dates[0]], True)  # vacant
            self.assertEqual(result[0]["availability"][mock_dates[1]], False)  # occupied
            
            # Check second hut
            self.assertEqual(result[1]["hut"], "Hut2")
            self.assertEqual(result[1]["availability"][mock_dates[0]], False)  # occupied
            self.assertEqual(result[1]["availability"][mock_dates[1]], True)  # vacant

    def test_locate_availability_no_huts(self):
        """Test when no huts are found."""
        with patch.object(self.scraper, '_locate_hut_names', return_value=[]):
            result = self.scraper.locate_availability()
            self.assertEqual(result, [])

    def test_locate_availability_no_dates(self):
        """Test when no dates are found."""
        with patch.object(self.scraper, '_locate_hut_names', return_value=["Hut1"]), \
             patch.object(self.scraper, '_locate_dates', return_value=[]):
            
            result = self.scraper.locate_availability()
            self.assertEqual(result, [])
            self.scraper.logger.error.assert_called_with("No dates found in table")

    def test_locate_availability_table_error(self):
        """Test handling of WebDriver exceptions."""
        mock_hut_names = ["Hut1"]
        mock_dates = [date(2024, 12, 25)]
        
        with patch.object(self.scraper, '_locate_hut_names', return_value=mock_hut_names), \
             patch.object(self.scraper, '_locate_dates', return_value=mock_dates), \
             patch('app.services.scraper.WebDriverWait') as mock_wait:
            
            mock_wait.return_value.until.side_effect = WebDriverException("Table not found")
            
            result = self.scraper.locate_availability()
            
            self.assertEqual(result, [])
            self.scraper.logger.error.assert_called_once()
            error_message = self.scraper.logger.error.call_args[0][0]
            self.assertIn("Error in locate_availability", error_message)

    def test_locate_availability_fewer_rows_than_huts(self):
        """Test handling of mismatched huts and rows."""
        mock_hut_names = ["Hut1", "Hut2"]
        mock_dates = [date(2024, 12, 25)]
        mock_table = MagicMock()
        mock_row = MagicMock()
        
        # Only return one row for two huts
        mock_row.find_elements.return_value = [MagicMock()]
        
        with patch.object(self.scraper, '_locate_hut_names', return_value=mock_hut_names), \
             patch.object(self.scraper, '_locate_dates', return_value=mock_dates), \
             patch('app.services.scraper.WebDriverWait') as mock_wait:
            
            mock_wait.return_value.until.return_value = [MagicMock(), mock_table]
            mock_table.find_elements.return_value = [MagicMock(), mock_row]  # Header + one data row
            
            result = self.scraper.locate_availability()
            
            self.assertEqual(len(result), 1)  # Should only process one hut
            self.assertEqual(result[0]["hut"], "Hut1")

    def test_scrape_success(self):
        """Test successful scraping operation."""
        mock_availability = [{"hut": "Test Hut", "availability": {}}]
        
        with patch.object(self.scraper, 'initialize_driver') as mock_init, \
             patch.object(self.scraper, 'select_winter_option') as mock_select, \
             patch.object(self.scraper, 'locate_availability', return_value=mock_availability):
            
            result = self.scraper.scrape()
            
            # Verify all methods were called
            mock_init.assert_called_once()
            mock_select.assert_called_once()
            self.assertEqual(result, mock_availability)

    def test_scrape_error(self):
        """Test error handling in scrape method."""
        with patch.object(self.scraper, 'initialize_driver', side_effect=Exception("Test error")):
            result = self.scraper.scrape()
            
            # Verify empty list is returned on error
            self.assertEqual(result, [])
            
            # Verify error was logged
            self.scraper.logger.error.assert_called_once()
            error_message = self.scraper.logger.error.call_args[0][0]
            self.assertIn("Error during scraping", error_message)

    def test_initialize_driver(self):
        """Test driver initialization."""
        with patch('app.services.scraper.webdriver.Chrome') as mock_chrome, \
             patch('app.services.scraper.Service') as mock_service, \
             patch('app.services.scraper.ChromeDriverManager') as mock_manager:
            
            mock_manager.return_value.install.return_value = "path/to/chromedriver"
            mock_chrome.return_value.get = MagicMock()
            
            self.scraper.initialize_driver()
            
            # Verify Chrome was initialized with correct options
            mock_chrome.assert_called_once()
            mock_chrome.return_value.get.assert_called_with("https://methowreservations.com/lodging/huts")
            self.scraper.logger.info.assert_called_with("Browser initialized and navigated to the target site.")

if __name__ == "__main__":
    unittest.main()
