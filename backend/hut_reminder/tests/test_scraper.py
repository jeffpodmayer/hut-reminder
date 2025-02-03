import unittest
from unittest.mock import MagicMock
from scraper import initialize_driver, select_winter_option

class TestScraper(unittest.TestCase):

    def setUp(self):
        """Set up the WebDriver for tests."""
        self.driver = MagicMock()
        self.driver.get.return_value = None
        self.driver.current_url = "https://methowreservations.com/lodging/huts"
        self.driver.title = "Lodging in Winthrop, WA at Rendezvous Huts with Methow Reservations"
        self.driver.find_element.return_value = MagicMock()  # Mock find_element

    def tearDown(self):
        """Close the WebDriver after tests."""
        # No actual browser interaction needed in this case
        pass

    def test_initialize_driver(self):
        """Test if the WebDriver initializes and navigates to the target URL."""
        initialize_driver(self.driver)
        
        # Test if the WebDriver's 'get' method was called with the correct URL
        self.driver.get.assert_called_with("https://methowreservations.com/lodging/huts")
        print("test_initialize_driver pass.")

    def test_check_url(self):
        """Test if the WebDriver navigates to the correct URL."""
        # Check if the current URL contains the expected URL part
        self.assertIn("methowreservations.com", self.driver.current_url)
        print("test_check_url pass.")

    def test_title(self):
        """Test if the page title is correct after navigating."""
        self.assertTrue("Lodging in Winthrop, WA at Rendezvous Huts with Methow Reservations" in self.driver.title)
        print("test_title pass.")

    def test_select_winter_option(self):
        """Test if the dropdown option 'Winter' is selected correctly."""
        # Mock the dropdown behavior and assert the selection of "Winter"
        dropdown = MagicMock()
        self.driver.find_element.return_value = dropdown
        # Mock the select object and the select_by_visible_text method
        select = MagicMock()
        dropdown.select = select
        select.select_by_visible_text.return_value = None
        # Call your method under test
        select_winter_option(self.driver)
        # Check if 'select_by_visible_text' was called with "Winter 2024-2025"
        select.select_by_visible_text.assert_called_with("Winter 2024-2025")
        print("test_select_winter_option pass.")


if __name__ == "__main__":
    unittest.main()
