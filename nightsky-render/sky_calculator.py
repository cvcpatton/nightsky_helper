# sky_calculator.py - Cathy Patton, 12/2/25, CSC 2017 Big Project (advanced feature)
# Handles astronomical calculations using Skyfield

from skyfield.api import load
from skyfield.almanac import find_discrete, dark_twilight_day
from datetime import datetime, timedelta
from models import Observation
from celestial_objects import CELESTIAL_OBJECTS, PLANET_MAP, STAR_COORDS
from location import DENVER, format_time
from moon import get_moon_illumination
import pytz

class SkyCalculator:
    def __init__(self):
        self.eph = load('de421.bsp')
        self.ts = load.timescale()
        self.observer = DENVER

    def calculate(self, obs_date: datetime.date) -> Observation:
        # Create observer location
        observer_loc = self.eph['earth'] + self.observer.topos

        # Local noon as aware datetime (pytz chooses correct MST/MDT automatically)
        local_noon = DENVER.tz.localize(datetime(obs_date.year, obs_date.month, obs_date.day, 12), is_dst=None)

        # Skyfield UTC times for event search (from local noon to two days later)
        t0 = self.ts.utc(local_noon.astimezone(pytz.utc))
        t1 = self.ts.utc((local_noon + timedelta(days=2)).astimezone(pytz.utc))

        # Use Skyfield's dark_twilight_day() to find sunset, twilight, and sunrise events
        f = dark_twilight_day(self.eph, self.observer.topos)
        times, events = find_discrete(t0, t1, f)

        # Convert all UTC times to Denver local time (aware)
        event_log = [(e, t.utc_datetime().astimezone(DENVER.tz)) for t, e in zip(times, events)]

        # Select sunset closest to local noon
        sunset_candidates = [lt for e, lt in event_log if e == 1]
        sunset = min(sunset_candidates, key=lambda lt: abs(lt - local_noon)) if sunset_candidates else None

        # Select astronomical twilight (dark_sky) after sunset
        dark_candidates = [lt for e, lt in event_log if e == 0 and sunset and lt > sunset]
        dark_start = min(dark_candidates, key=lambda lt: (lt - sunset).total_seconds()) if dark_candidates else None

        # Select sunrise the next day
        sunrise_candidates = [lt for e, lt in event_log if e == 3 and lt > sunset]
        sunrise = min(sunrise_candidates, key=lambda lt: (lt - sunset).total_seconds()) if sunrise_candidates else None

        # Determine which planets are visible above the horizon at 10 PM local time
        night_time_local = DENVER.tz.localize(datetime(obs_date.year, obs_date.month, obs_date.day, 22), is_dst=None)
        t_night = self.ts.utc(night_time_local.astimezone(pytz.utc))

        visible_planets = [
            name for name in CELESTIAL_OBJECTS['planets']
            if (eph_name := PLANET_MAP.get(name)) and eph_name in self.eph
            and observer_loc.at(t_night).observe(self.eph[eph_name]).apparent().altaz()[0].degrees > 0
        ]

        # Determine which stars are visible above the horizon at 10 PM local time
        visible_stars = [
            name for name in CELESTIAL_OBJECTS['stars']
            if (star := STAR_COORDS.get(name)) and
            observer_loc.at(t_night).observe(star).apparent().altaz()[0].degrees > 0
        ]

        # Moon illumination
        moon_illum = get_moon_illumination(obs_date)

        # Return observation data
        return Observation(
            date=obs_date.isoformat(),
            sunset=format_time(sunset),
            dark_sky=format_time(dark_start),
            sunrise=format_time(sunrise),
            planets=visible_planets,
            stars=visible_stars,
            moon_illum=moon_illum
        )
