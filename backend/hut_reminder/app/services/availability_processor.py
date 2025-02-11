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

def add_huts_and_availability_to_database():
    scraper = Scraper.new()  # Create a new Scraper instance
    scraper.initialize_driver()  # Initialize the WebDriver

    try:
        hut_names, availability_data = scraper.scrape()  # Call the scrape method
        print(hut_names)  # Print the hut names for verification
    except Exception as e:
        print(f"Error while scraping: {e}")
        return  # Exit the function if there's an error

    add_huts(hut_names)  # Call the method to add huts
    add_availability(availability_data)  # Call the method to add availability

def add_huts(hut_names):
    for hut_name in hut_names:
        existing_hut = db.session.query(Hut).filter_by(name=hut_name).first()
        
        if not existing_hut:
            # If the hut does not exist, create it
            existing_hut = Hut(name=hut_name)
            db.session.add(existing_hut)
            print(f"Added hut: {existing_hut.name}")  # Print the name of the hut being added

    try:
        db.session.commit()  # Commit the session to save changes
        print(f"Added {len(hut_names)} huts to the database.")
    except Exception as e:
        print(f"Error committing huts to the database: {e}")
        db.session.rollback()  # Rollback the session in case of error

def add_availability(availability_data):
    for entry in availability_data:
        hut_name = entry['hut']
        existing_hut = db.session.query(Hut).filter_by(name=hut_name).first()
        
        if existing_hut:
            # Now add or update the availability for this hut
            for date, is_vacant in entry['availability'].items():
                # Check if the availability record already exists
                existing_availability = db.session.query(Availability).filter_by(
                    hut_id=existing_hut.id,
                    date=date
                ).first()
                
                if existing_availability:
                    # If the record exists, check if the is_vacant value has changed
                    if existing_availability.is_vacant != is_vacant:
                        existing_availability.is_vacant = is_vacant  # Update the value
                        print(f"Updated availability for {hut_name} on {date} to {'vacant' if is_vacant else 'not vacant'}.")
                else:
                    # If the record does not exist, create a new availability record
                    availability_record = Availability(
                        hut_id=existing_hut.id,
                        date=date,
                        is_vacant=is_vacant
                    )
                    db.session.add(availability_record)  # Add availability record to the session
                    print(f"Added availability for {hut_name} on {date} as {'vacant' if is_vacant else 'not vacant'}.")
    
    try:
        db.session.commit()  # Commit the session to save changes
        print(f"Added/Updated availability data in the database.")
    except Exception as e:
        print(f"Error committing availability to the database: {e}")
        db.session.rollback()  # Rollback the session in case of error
