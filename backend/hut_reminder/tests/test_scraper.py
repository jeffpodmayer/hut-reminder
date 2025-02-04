import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from ..hut_reminder.services.scraper import Scraper

class TestScraper(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scraper = Scraper.new()
        self.scraper.driver = MagicMock()
        # Mock the basic driver attributes
        self.scraper.driver.current_url = "https://methowreservations.com/lodging/huts"
        self.scraper.driver.title = "Lodging in Winthrop, WA at Rendezvous Huts with Methow Reservations"

    def tearDown(self):
        """Clean up after each test method."""
        if hasattr(self.scraper, 'driver'):
            self.scraper.driver.quit()

    def test_initialization(self):
        """Test if Scraper initializes correctly."""
        self.assertIsInstance(self.scraper, Scraper)
        self.assertIsNotNone(self.scraper.logger)

    # def test_initialize_driver(self):
    #     """Test if the WebDriver initializes and navigates to the target URL."""
    #     initialize_driver(self.scraper.driver)
        
    #     # Test if the WebDriver's 'get' method was called with the correct URL
    #     self.scraper.driver.get.assert_called_with("https://methowreservations.com/lodging/huts")
    #     print("test_initialize_driver pass.")

    # def test_check_url(self):
    #     """Test if the WebDriver navigates to the correct URL."""
    #     # Check if the current URL contains the expected URL part
    #     self.assertIn("methowreservations.com", self.scraper.driver.current_url)
    #     print("test_check_url pass.")

    # def test_title(self):
    #     """Test if the page title is correct after navigating."""
    #     self.assertTrue("Lodging in Winthrop, WA at Rendezvous Huts with Methow Reservations" in self.scraper.driver.title)
    #     print("test_title pass.")

    # def test_select_winter_option(self):
    #     """Test if the dropdown option 'Winter' is selected correctly."""
    #     # Mock the dropdown behavior and assert the selection of "Winter"
    #     dropdown = MagicMock()
    #     self.scraper.driver.find_element.return_value = dropdown
    #     # Mock the select object and the select_by_visible_text method
    #     select = MagicMock()
    #     dropdown.select = select
    #     select.select_by_visible_text.return_value = None
    #     # Call your method under test
    #     select_winter_option(self.scraper.driver)
    #     # Check if 'select_by_visible_text' was called with "Winter 2024-2025"
    #     select.select_by_visible_text.assert_called_with("Winter 2024-2025")
    #     print("test_select_winter_option pass.")


if __name__ == "__main__":
    unittest.main()
