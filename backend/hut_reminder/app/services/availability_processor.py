# Process availability data from the scraper and save to database

# Required imports will include:
from datetime import datetime
from logging import getLogger
from typing import List, Dict
from scraper import Scraper

from app.models.hut import Hut
from app.models.availability import Availability


class AvailabilityProcessor:
    """
    Process hut availability data and save to database.
    
    Main responsibilities:
    - Take raw availability data from scraper
    - Format data for database storage
    - Update or create hut records
    - Update or create availability records
    - Handle any data conflicts or updates
    """
    
    # TODO: Add methods for:
    # - Processing scraped data
    # - Updating hut information
    # - Updating availability records
    # - Cleaning up old records
    # - Handling errors/logging
    
    # TODO: Add database session management
    # TODO: Add example usage in __main__ block

# GOt through object from the scraper and get the hut objects
# Query for huts with name and for any that dotn exist, create them


# Big Bang query for all the availability objects
# In Code:
# GO tthrough all object and date model you got from Scraper
# Loop tgrough the availabity data adn create availablit ibject for Hut, Date and is_Vacant
# Compare them and see if the availablitty changed
# Trigger a remider and change the availablity object to refeclt the change
# Save the object to the database




if __name__ == "__main__":
    scraper = Scraper.new()
    data = scraper.scrape()
    processor = AvailabilityProcessor()
    # Create process_availability method
    processor.process_availability(data) 