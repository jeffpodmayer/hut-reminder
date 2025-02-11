# Process availability data from the scraper and save to database

# Required imports will include:
from datetime import datetime
from logging import getLogger
from typing import List, Dict
from .scraper import Scraper

from .. import db  # Correctly import the db instance
from ..models.hut import Hut  # Import the Hut model

from ..models.availability import Availability


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

def add_huts_to_database():
    scraper = Scraper.new()  # Create a new Scraper instance
    scraper.initialize_driver()  # Initialize the WebDriver

    try:
        hut_names = scraper._locate_hut_names()  # Call the method to get hut names
        print(hut_names)  # Print the hut names for verification
    except Exception as e:
        print(f"Error while locating hut names: {e}")
        return  # Exit the function if there's an error

    for hut_name in hut_names:
        # Check if the hut already exists in the database
        existing_hut = db.session.query(Hut).filter_by(name=hut_name).first()
        if existing_hut:
            print(f"Hut '{hut_name}' already exists. Skipping.")
            continue  # Skip adding this hut if it already exists

        # Create a new Hut instance
        new_hut = Hut(name=hut_name)  # Use the name field from the Hut model
        db.session.add(new_hut)  # Add the new hut to the session
        print(f"Added hut: {new_hut.name}")  # Print the name of the hut being added

    try:
        db.session.commit()  # Commit the session to save changes
        print(f"Added {len(hut_names)} huts to the database.")
    except Exception as e:
        print(f"Error committing to the database: {e}")
        db.session.rollback()  # Rollback the session in case of error
