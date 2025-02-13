from datetime import datetime
from logging import getLogger
from typing import List, Dict
from .scraper import Scraper
from .. import db  
from ..models.hut import Hut 
from ..models.availability import Availability


class AvailabilityProcessor:
    """Process hut availability data and save to database."""
def add_huts_and_availability_to_database():
    scraper = Scraper.new()  
    scraper.initialize_driver()  

    try:
        hut_names, availability_data = scraper.scrape()  
        print(hut_names)  
    except Exception as e:
        print(f"Error while scraping: {e}")
        return  

    add_huts(hut_names)  
    add_availability(availability_data) 

def add_huts(hut_names):
    for hut_name in hut_names:
        existing_hut = db.session.query(Hut).filter_by(name=hut_name).first()
        
        if not existing_hut:
            # If the hut does not exist, create it
            existing_hut = Hut(name=hut_name)
            db.session.add(existing_hut)
            print(f"Added hut: {existing_hut.name}")  

    try:
        db.session.commit()  
        print(f"All existing huts have been added to the database.")
    except Exception as e:
        print(f"Error committing huts to the database: {e}")
        db.session.rollback() 

def add_availability(availability_data):
    for entry in availability_data:
        hut_name = entry['hut']
        existing_hut = db.session.query(Hut).filter_by(name=hut_name).first()
        
        if existing_hut:
            process_hut_availability(existing_hut, entry['availability'])

    try:
        db.session.commit() 
        print(f"Added/Updated availability data in the database.")
    except Exception as e:
        print(f"Error committing availability to the database: {e}")
        db.session.rollback()  

def process_hut_availability(existing_hut, availability):
    for date, is_vacant in availability.items():
        existing_availability = db.session.query(Availability).filter_by(
            hut_id=existing_hut.id,
            date=date
        ).first()
        
        if existing_availability:
            update_availability(existing_availability, is_vacant, existing_hut.name, date)
        else:
            create_availability(existing_hut.id, date, is_vacant)

def update_availability(existing_availability, is_vacant, hut_name, date):
    if existing_availability.is_vacant != is_vacant:
        existing_availability.is_vacant = is_vacant  # Update the value
        print(f"Updated availability for {hut_name} on {date} to {'vacant' if is_vacant else 'not vacant'}.")

def create_availability(hut_id, date, is_vacant):
    availability_record = Availability(
        hut_id=hut_id,
        date=date,
        is_vacant=is_vacant
    )
    db.session.add(availability_record)  # Add availability record to the session
    print(f"Added availability for hut on {date} as {'vacant' if is_vacant else 'not vacant'}.")
