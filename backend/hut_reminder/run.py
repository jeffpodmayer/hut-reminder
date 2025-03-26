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

def setup_scheduler(interval_seconds=30):  # Default to 30 seconds for testing
    """Set up the scheduler to run the scraper at specified interval"""
    # Use SQLAlchemy for persistent job storage
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    
    scheduler = BackgroundScheduler(jobstores=jobstores)
    
    # For testing: run every 30 seconds or 2 minutes (120 seconds)
    scheduler.add_job(
        run_scraper, 
        'interval', 
        seconds=interval_seconds,  # Use seconds parameter for short intervals
        id='scraper_job', 
        replace_existing=True, 
        misfire_grace_time=10  # Shorter grace time for testing
    )
    
    scheduler.start()
    logger.info(f"Scheduler started - running every {interval_seconds} seconds")
    
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
