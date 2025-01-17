import unittest
from scraper import initialize_driver

class TestScraper(unittest.TestCase):

    def setUp(self):
        """Set up the WebDriver for tests."""
        print("Initializing driver...")
        self.driver = initialize_driver()

    def tearDown(self):
        """Close the WebDriver after tests."""
        print("Closing driver...")
        self.driver.quit()

    def test_driver_initialization(self):
        """Test if the WebDriver initializes and navigates to the target URL."""
        print("Checking the current URL...")
        self.assertIn("methowreservations.com", self.driver.current_url)

    def test_title(self):
        """Test if the page title is correct after navigating."""
        print("Checking the page title...")
        self.assertTrue("Lodging Huts" in self.driver.title)

if __name__ == "__main__":
    unittest.main()
