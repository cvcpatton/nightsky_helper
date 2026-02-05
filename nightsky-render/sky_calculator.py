# sky_calculator.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Handles astronomical calculations using Skyfield

from skyfield.api import load, Star, Topos
from skyfield.almanac import find_discrete, dark_twilight_day
from datetime import datetime, timedelta, date
import pytz
from models import Observation
from celestial_objects import CELESTIAL_OBJECTS, PLANET_MAP, STAR_COORDS
from location import DENVER, format_time
from moon import get_moon_illumination


class SkyCalculator:
    # Handles astronomy calculations and clarifies Skyfield terminology for the user.

    def __init__(self):
        self.eph = load('de421.bsp')
        self.ts = load.timescale()
        self.tz = DENVER.tz
        self.observer = DENVER

    def calculate(self, obs_date: date) -> Observation:
        # Calculate stargazing conditions for a given date (DST-aware)

        observer_loc = self.eph['earth'] + self.observer.topos

        # Local noon in Denver
        local_noon = self.tz.localize(datetime(obs_date.year, obs_date.month, obs_date.day, 12), is_dst=None)

        # Two-day interval for dark_twilight_day
        t0 = self.ts.utc(local_noon.astimezone(pytz.utc))
        t1 = self.ts.utc((local_noon + timedelta(days=2)).astimezone(pytz.utc))

        # Get twilight/sunset events
        f = dark_twilight_day(self.eph, self.observer.topos)
        times, events = find_discrete(t0, t1, f)

        # Convert Skyfield times to localized datetime objects
        event_log = [
            (e, t.utc_datetime().replace(tzinfo=pytz.utc).astimezone(self.tz))
            for t, e in zip(times, events)
        ]

        # Sunset on the observation date
        sunset = next(
            (lt for e, lt in reversed(event_log) if e == 1 and lt.date() == obs_date),
            None
        )

        # Dark sky start (after sunset)
        dark_start = next(
            (lt for e, lt in event_log if e == 0 and sunset and lt > sunset and lt.date() == obs_date),
            None
        )

        # Sunrise on the following day
        sunrise = next(
            (lt for e, lt in event_log if e == 3 and lt.date() == obs_date + timedelta(days=1)),
            None
        )

        # Local 10 PM for checking visibility
        local_night = self.tz.localize(datetime(obs_date.year, obs_date.month, obs_date.day, 22), is_dst=None)
        t_night = self.ts.utc(local_night.astimezone(pytz.utc))

        # Determine visible planets at 10 PM
        visible_planets = [
            name for name in CELESTIAL_OBJECTS['planets']
            if (eph_name := PLANET_MAP.get(name)) and eph_name in self.eph
            and observer_loc.at(t_night).observe(self.eph[eph_name]).apparent().altaz()[0].degrees > 0
        ]

        # Determine visible stars at 10 PM
        visible_stars = [
            name for name in CELESTIAL_OBJECTS['stars']
            if (star := STAR_COORDS.get(name)) and observer_loc.at(t_night).observe(star).apparent().altaz()[0].degrees > 0
        ]

        # Get moon illumination
        moon_illum = get_moon_illumination(obs_date)

        # Return all relevant observation data
        return Observation(
            date=obs_date.isoformat(),
            sunset=format_time(sunset),
            dark_sky=format_time(dark_start),
            sunrise=format_time(sunrise),
            planets=visible_planets,
            stars=visible_stars,
            moon_illum=moon_illum
        )

