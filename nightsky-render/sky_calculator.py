# sky_calculator.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Handles astronomical calculations using Skyfield

# Import modules to support program execution and celestial data dictionaries from celestial_objects.py
from skyfield.api import load
from datetime import datetime, date
from astral import LocationInfo, Depression
from astral.sun import sun, dusk
import pytz
from models import Observation
from celestial_objects import CELESTIAL_OBJECTS, PLANET_MAP, STAR_COORDS
from location import DENVER, to_utc, format_time
from moon import get_moon_illumination

class SkyCalculator:
    # Handles astronomy calculations and clarifies Skyfield terminology for the user
    def __init__(self):
        self.eph = load('de421.bsp')
        self.ts = load.timescale()
        self.observer = DENVER
        self.city = LocationInfo(
            "Denver",
            "USA",
            "America/Denver",
            DENVER.latitude,
            DENVER.longitude
        )

    def calculate(self, obs_date: date) -> Observation:
        # Use Skyfield library to calculate visible planets and stars

        observer_loc = self.eph['earth'] + self.observer.topos

        tz = self.observer.tz

        sun_times = sun(
            self.city.observer,
            date=obs_date,
            tzinfo=tz
        )
        sunset = sun_times["sunset"]
        sunrise = sun_times["sunrise"]
        dark_start = dusk(
            self.city.observer,
            date=obs_date,
            depression=Depression.ASTRONOMICAL,
            tzinfo=tz
        )

        # Define the time for checking visibility: 10:00 PM local time on the observation date
        t_night = self.ts.utc(to_utc(datetime(obs_date.year, obs_date.month, obs_date.day, 22)))

        # Determine which planets are visible above the horizon at 10 PM
        visible_planets = [
            name for name in CELESTIAL_OBJECTS['planets']
            if (eph_name := PLANET_MAP.get(name)) and eph_name in self.eph
            and observer_loc.at(t_night).observe(self.eph[eph_name]).apparent().altaz()[0].degrees > 0
        ]

        # Determine which stars are visible above the horizon at 10 PM
        visible_stars = [
            name for name in CELESTIAL_OBJECTS['stars']
            if (star := STAR_COORDS.get(name)) and
            observer_loc.at(t_night).observe(star).apparent().altaz()[0].degrees > 0
        ]

        # New feature: added moon illumination data via web scraping
        moon_illum = get_moon_illumination(obs_date)

        # Return all relevant stargazing data
        return Observation(
            date=obs_date.isoformat(),
            sunset=format_time(sunset),
            dark_sky=format_time(dark_start),
            sunrise=format_time(sunrise),
            planets=visible_planets,
            stars=visible_stars,
            moon_illum=moon_illum
        )
