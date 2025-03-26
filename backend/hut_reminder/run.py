from app import create_app
from app.services.availability_processor import add_huts_and_availability_to_database
from app.routes.hut_routes import hut_routes
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging
import atexit

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = create_app()

def run_scraper():
    """Function to run the scraper and update the database"""
    try:
        logger.info("Starting scheduled scraper run")
        with app.app_context():
            add_huts_and_availability_to_database()
        logger.info("Scraper completed successfully")
    except Exception as e:
        logger.error(f"Error running scraper: {e}", exc_info=True)

def setup_scheduler(interval_seconds=None, interval_hours=None):
    """
    Set up the scheduler to run the scraper at specified interval.
    
    Args:
        interval_seconds: Run interval in seconds (for testing)
        interval_hours: Run interval in hours (for production)
    """
    # Use SQLAlchemy for persistent job storage
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    
    scheduler = BackgroundScheduler(jobstores=jobstores)
    
    # Determine the interval type and value
    if interval_seconds is not None:
        # For testing: use seconds
        scheduler.add_job(
            run_scraper, 
            'interval', 
            seconds=interval_seconds,
            id='scraper_job', 
            replace_existing=True, 
            misfire_grace_time=10  # Short grace time for testing
        )
        logger.info(f"Scheduler started - running every {interval_seconds} seconds (TESTING MODE)")
    else:
        # For production: use hours (default to 8 if not specified)
        hours = interval_hours if interval_hours is not None else 8
        scheduler.add_job(
            run_scraper, 
            'interval', 
            hours=hours,
            id='scraper_job', 
            replace_existing=True, 
            misfire_grace_time=600  # 10 minutes grace time
        )
        logger.info(f"Scheduler started - running every {hours} hours")
    
    scheduler.start()
    
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    
    return scheduler

if __name__ == '__main__':
    # Run the scraper once at startup
    with app.app_context():
        add_huts_and_availability_to_database()
    
    # Set up the scheduler to run every 30 seconds for testing
    # Change to 120 for 2 minutes
    scheduler = setup_scheduler(interval_seconds=30)  # 30 seconds
    # scheduler = setup_scheduler(interval_seconds=120)  # 2 minutes
    
    # Run the Flask app
    app.run(debug=True)
