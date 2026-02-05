# sky_calculator.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Handles astronomical calculations using Skyfield

# Import modules to support program execution and celestial data dictionaries from celestial_objects.py
from skyfield.api import load, Star, Topos
from skyfield.almanac import find_discrete, dark_twilight_day
from datetime import datetime, timedelta
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

    def calculate(self, obs_date: datetime.date) -> Observation:
        # Use Skyfield library to calculate visible planets and stars

        observer_loc = self.eph['earth'] + self.observer.topos

        # Set up two time points for event search: noon of the observation day and 2 days later
        local_noon = datetime(obs_date.year, obs_date.month, obs_date.day, 12)
        t0 = self.ts.utc(to_utc(local_noon))
        t1 = self.ts.utc(to_utc(local_noon + timedelta(days=2)))

        # Use Skyfield's dark_twilight_day() function to find sunset, darkness, and sunrise events
        f = dark_twilight_day(self.eph, self.observer.topos)
        times, events = find_discrete(t0, t1, f)

        # Create a list of (event_type, local_time) tuples for easier filtering
        event_log = [(e, t.utc_datetime().astimezone(self.observer.tz)) for t, e in zip(times, events)]

        # Pick the sunset closest to local noon
        sunset = min((lt for e, lt in event_log if e == 1), key=lambda lt: abs(lt - local_noon))

        # Pick the dark_sky (astronomical twilight) **after sunset**
        dark_start = min((lt for e, lt in event_log if e == 0 and lt > sunset), key=lambda lt: lt - sunset)

        # Pick sunrise the next day
        sunrise = min((lt for e, lt in event_log if e == 3 and lt > sunset), key=lambda lt: lt - sunset)

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


