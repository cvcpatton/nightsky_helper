# location.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Location and timezone handling, Location class, Denver subclass

# Import modules to support program execution
from skyfield.api import Topos
import pytz

# Base Location class
class Location:
    def __init__(self, latitude: float, longitude: float, tz_name: str):
        self.latitude = latitude
        self.longitude = longitude
        self.tz = pytz.timezone(tz_name)
        self.topos = Topos(latitude_degrees=latitude, longitude_degrees=longitude)

    # Method to allow overriding
    def description(self):
        return f"Generic location at lat {self.latitude}, lon {self.longitude}"

# Denver child class, inherits from Location
class Denver(Location):
    # Variables for Denver coordinates
    def __init__(self):
        super().__init__(latitude=39.7392, longitude=-104.9903, tz_name='America/Denver')

    # Override description to show Denver-specific coordinates
    def description(self):
        return f"Denver location: lat {self.latitude}, lon {self.longitude}"

# Singleton Denver instance for simplicity
DENVER = Denver()

def to_utc(local_dt):
    # Convert localized datetime to UTC
    return DENVER.tz.localize(local_dt).astimezone(pytz.utc)

def format_time(dt):
    # Formatted time for clean output (12-hour format with AM/PM and no leading zeroes)
    return dt.strftime("%I:%M %p").lstrip("0") if dt else "Unavailable"
