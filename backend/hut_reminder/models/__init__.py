from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .hut import Hut
from .availability import Availability
from .reminder import Reminder

# This allows importing from models directly
__all__ = ['db', 'Hut', 'Availability', 'Reminder'] 